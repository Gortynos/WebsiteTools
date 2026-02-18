import logging
import os

from flask import Flask
from extensions import limiter


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    logging.basicConfig(
        level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)
    )

    app.config["TASKS_FILE"] = os.path.join("base", "todo_list.json")
    app.config["UPLOAD_FOLDER"] = "uploads"
    app.config["SPLIT_FOLDER"] = os.path.join("static", "split_pdfs")
    app.config["MERGED_FOLDER"] = os.path.join("static", "merged_pdfs")
    app.config["MAX_PDF_SIZE_BYTES"] = int(os.getenv("MAX_PDF_SIZE_MB", "10")) * 1024 * 1024
    app.config["MAX_MERGE_TOTAL_SIZE_BYTES"] = int(
        os.getenv("MAX_MERGE_TOTAL_PDF_SIZE_MB", "30")
    ) * 1024 * 1024
    app.config["MAX_MERGE_FILES"] = int(os.getenv("MAX_MERGE_FILES", "20"))
    app.config["ALLOWED_PDF_EXTENSIONS"] = {".pdf"}
    app.config["ALLOWED_PDF_MIME_TYPES"] = {"application/pdf", "application/x-pdf"}
    app.config["RATELIMIT_HEADERS_ENABLED"] = True
    app.config["RATELIMIT_STORAGE_URI"] = os.getenv("RATELIMIT_STORAGE_URI", "memory://")

    os.makedirs("base", exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["SPLIT_FOLDER"], exist_ok=True)
    os.makedirs(app.config["MERGED_FOLDER"], exist_ok=True)
    limiter.init_app(app)

    from blueprints.pages import pages_bp
    from blueprints.password import password_bp
    from blueprints.pdf import pdf_bp
    from blueprints.text_diff import text_diff_bp
    from blueprints.todo import todo_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(text_diff_bp)
    return app


app = create_app()

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "").strip().lower() in {"1", "true", "yes", "on"}
    app.run(debug=debug_mode)
