import os
import uuid

import fitz
from flask import Blueprint, current_app, jsonify, request, url_for
from werkzeug.utils import secure_filename
from extensions import limiter
from i18n import t

pdf_bp = Blueprint("pdf_api", __name__)


def split_pdf(input_pdf, output_folder):
    split_files = []
    upload_id = os.path.basename(output_folder)

    with fitz.open(input_pdf) as doc:
        for i in range(doc.page_count):
            with fitz.open() as new_pdf:
                new_pdf.insert_pdf(doc, from_page=i, to_page=i)
                output_filename = f"page_{i + 1}.pdf"
                output_path = os.path.join(output_folder, output_filename)
                new_pdf.save(output_path)
                split_files.append(
                    url_for("static", filename=f"split_pdfs/{upload_id}/{output_filename}")
                )

    return split_files


def merge_pdfs(input_files, output_pdf_path):
    with fitz.open() as merged_pdf:
        for input_file in input_files:
            with fitz.open(input_file) as source_pdf:
                merged_pdf.insert_pdf(source_pdf)
        merged_pdf.save(output_pdf_path)


def extract_pdf_text(input_pdf):
    pages = []
    with fitz.open(input_pdf) as doc:
        for idx, page in enumerate(doc, start=1):
            pages.append({"page": idx, "text": page.get_text("text")})
    return pages


def is_allowed_pdf(file_storage):
    filename = (file_storage.filename or "").lower()
    ext = os.path.splitext(filename)[1]
    if ext not in current_app.config["ALLOWED_PDF_EXTENSIONS"]:
        return False

    mimetype = (file_storage.mimetype or "").lower()
    if mimetype and mimetype not in current_app.config["ALLOWED_PDF_MIME_TYPES"]:
        return False
    return True


def get_uploaded_file_size(file_storage):
    stream = file_storage.stream
    current_pos = stream.tell()
    stream.seek(0, os.SEEK_END)
    size = stream.tell()
    stream.seek(current_pos)
    return size


def save_upload_file(file_storage, output_dir, fallback_name):
    filename = secure_filename(file_storage.filename)
    if not filename:
        filename = fallback_name

    output_path = os.path.join(output_dir, filename)
    file_storage.save(output_path)
    return output_path


@pdf_bp.route("/api/split_pdf", methods=["POST"])
@limiter.limit("10 per minute")
@limiter.limit("50 per hour")
def split_pdf_api():
    if "file" not in request.files:
        return jsonify({"error": t("pdf.no_file_uploaded")}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": t("pdf.no_file_selected")}), 400

    if not is_allowed_pdf(file):
        return jsonify({"error": t("pdf.only_pdf_allowed")}), 400

    file_size = get_uploaded_file_size(file)
    max_size = current_app.config["MAX_PDF_SIZE_BYTES"]
    if file_size > max_size:
        return jsonify({"error": t("pdf.file_too_large", size_mb=max_size // (1024 * 1024))}), 400

    filename = secure_filename(file.filename)
    if not filename:
        return jsonify({"error": t("pdf.invalid_filename")}), 400

    upload_id = uuid.uuid4().hex
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_id)
    split_dir = os.path.join(current_app.config["SPLIT_FOLDER"], upload_id)
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(split_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    try:
        file.save(file_path)
        split_files = split_pdf(file_path, split_dir)
    except (fitz.FileDataError, ValueError):
        current_app.logger.warning("Uploaded file is not a valid PDF: %s", filename)
        return jsonify({"error": t("pdf.invalid_pdf")}), 400
    except OSError:
        current_app.logger.exception("Filesystem error while processing PDF upload.")
        return jsonify({"error": t("pdf.storage_error_file")}), 500

    return jsonify({"message": t("pdf.split_success"), "files": split_files})


@pdf_bp.route("/api/merge_pdf", methods=["POST"])
@limiter.limit("6 per minute")
@limiter.limit("30 per hour")
def merge_pdf_api():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": t("pdf.no_files_uploaded")}), 400
    if len(files) < 2:
        return jsonify({"error": t("pdf.min_two_files")}), 400
    if len(files) > current_app.config["MAX_MERGE_FILES"]:
        return jsonify(
            {"error": t("pdf.too_many_files", max_files=current_app.config["MAX_MERGE_FILES"])}
        ), 400

    max_file_size = current_app.config["MAX_PDF_SIZE_BYTES"]
    max_total_size = current_app.config["MAX_MERGE_TOTAL_SIZE_BYTES"]
    total_size = 0

    for file in files:
        if not file.filename:
            return jsonify({"error": t("pdf.invalid_uploaded_filename")}), 400
        if not is_allowed_pdf(file):
            return jsonify({"error": t("pdf.only_pdf_allowed")}), 400

        file_size = get_uploaded_file_size(file)
        if file_size > max_file_size:
            return jsonify(
                {"error": t("pdf.single_file_too_large", size_mb=max_file_size // (1024 * 1024))}
            ), 400
        total_size += file_size

    if total_size > max_total_size:
        return jsonify(
            {"error": t("pdf.total_upload_too_large", size_mb=max_total_size // (1024 * 1024))}
        ), 400

    upload_id = uuid.uuid4().hex
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_id)
    merge_dir = os.path.join(current_app.config["MERGED_FOLDER"], upload_id)
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(merge_dir, exist_ok=True)

    saved_files = []
    try:
        for idx, file in enumerate(files, start=1):
            saved_files.append(save_upload_file(file, upload_dir, f"file_{idx}.pdf"))

        output_filename = "merged.pdf"
        output_path = os.path.join(merge_dir, output_filename)
        merge_pdfs(saved_files, output_path)
    except (fitz.FileDataError, ValueError):
        current_app.logger.warning("Uploaded file set contains invalid PDF data.")
        return jsonify({"error": t("pdf.invalid_pdf_in_set")}), 400
    except OSError:
        current_app.logger.exception("Filesystem error while processing PDF merge.")
        return jsonify({"error": t("pdf.storage_error_files")}), 500

    merged_file_url = url_for("static", filename=f"merged_pdfs/{upload_id}/{output_filename}")
    return jsonify({"message": t("pdf.merge_success"), "file": merged_file_url})


@pdf_bp.route("/api/extract_pdf_text", methods=["POST"])
@limiter.limit("10 per minute")
@limiter.limit("50 per hour")
def extract_pdf_text_api():
    if "file" not in request.files:
        return jsonify({"error": t("pdf.no_file_uploaded")}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": t("pdf.no_file_selected")}), 400
    if not is_allowed_pdf(file):
        return jsonify({"error": t("pdf.only_pdf_allowed")}), 400

    file_size = get_uploaded_file_size(file)
    max_size = current_app.config["MAX_PDF_SIZE_BYTES"]
    if file_size > max_size:
        return jsonify({"error": t("pdf.file_too_large", size_mb=max_size // (1024 * 1024))}), 400

    output_format = (request.form.get("output_format", "text") or "text").lower()
    if output_format not in {"text", "json"}:
        output_format = "text"

    upload_id = uuid.uuid4().hex
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], upload_id)
    os.makedirs(upload_dir, exist_ok=True)
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_dir, filename or "input.pdf")

    try:
        file.save(file_path)
        pages = extract_pdf_text(file_path)
    except (fitz.FileDataError, ValueError):
        current_app.logger.warning("Uploaded file is not a valid PDF: %s", file.filename)
        return jsonify({"error": t("pdf.invalid_pdf")}), 400
    except OSError:
        current_app.logger.exception("Filesystem error while extracting PDF text.")
        return jsonify({"error": t("pdf.storage_error_file")}), 500

    if output_format == "json":
        return jsonify(
            {
                "message": t("pdf.extract_success"),
                "format": "json",
                "pages": pages,
            }
        )

    text = "\n\n".join(page["text"] for page in pages if page["text"])
    return jsonify(
        {
            "message": t("pdf.extract_success"),
            "format": "text",
            "text": text,
        }
    )
