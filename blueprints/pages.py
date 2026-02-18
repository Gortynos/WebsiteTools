from flask import Blueprint, render_template

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html")


@pages_bp.route("/todo")
@pages_bp.route("/todo/")
def todo_page():
    return render_template("todo.html")


@pages_bp.route("/password")
@pages_bp.route("/password/")
def password_page():
    return render_template("password.html")


@pages_bp.route("/password-strength")
@pages_bp.route("/password-strength/")
def password_strength_page():
    return render_template("password_strength.html")


@pages_bp.route("/split-pdf")
@pages_bp.route("/split-pdf/")
def split_pdf_page():
    return render_template("split_pdf.html")


@pages_bp.route("/extract-pdf-text")
@pages_bp.route("/extract-pdf-text/")
def extract_pdf_text_page():
    return render_template("extract_pdf_text.html")


@pages_bp.route("/text-diff")
@pages_bp.route("/text-diff/")
def text_diff_page():
    return render_template("text_diff.html")
