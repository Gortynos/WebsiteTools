from flask import request

SUPPORTED_LANGUAGES = {"pl", "en"}
DEFAULT_LANGUAGE = "pl"

TRANSLATIONS = {
    "pl": {
        "todo.description_required": "Opis zadania jest wymagany.",
        "todo.task_added": "Zadanie dodane.",
        "todo.task_deleted": "Zadanie usuniete.",
        "todo.task_updated": "Zadanie zaktualizowane.",
        "todo.invalid_task_id": "Nieprawidlowe ID zadania.",
        "password.length_min": "Dlugosc hasla musi miec co najmniej 4 znaki.",
        "password.character_type_required": "Wybierz co najmniej jeden typ znakow.",
        "password.length_integer": "Dlugosc musi byc liczba calkowita.",
        "password_strength.password_required": "Hasło jest wymagane.",
        "password_strength.score_0": "Bardzo słabe",
        "password_strength.score_1": "Słabe",
        "password_strength.score_2": "Średnie",
        "password_strength.score_3": "Dobre",
        "password_strength.score_4": "Bardzo dobre",
        "password_strength.recommended_note": "Najbardziej realistyczny dla typowej aplikacji webowej jest zwykle scenariusz online z ograniczeniami prób.",
        "password_strength.scenario.online_throttled.label": "Online z limitem prób",
        "password_strength.scenario.online_throttled.description": "Atak przez formularz logowania z limitami i blokadami.",
        "password_strength.scenario.online_unthrottled.label": "Online bez limitu",
        "password_strength.scenario.online_unthrottled.description": "Atak online bez skutecznego ograniczania prób.",
        "password_strength.scenario.offline_slow_hashing.label": "Offline, wolne hashowanie",
        "password_strength.scenario.offline_slow_hashing.description": "Wyciek bazy i atak na kosztowny hash (bcrypt/argon2).",
        "password_strength.scenario.offline_fast_hashing.label": "Offline, szybkie hashowanie",
        "password_strength.scenario.offline_fast_hashing.description": "Wyciek bazy i atak GPU na szybki hash.",
        "password_strength.unknown": "nieznany",
        "pdf.no_file_uploaded": "Nie przeslano pliku.",
        "pdf.no_file_selected": "Nie wybrano pliku.",
        "pdf.only_pdf_allowed": "Dozwolone sa tylko pliki PDF.",
        "pdf.file_too_large": "Plik jest za duzy. Maksymalny rozmiar to {size_mb} MB.",
        "pdf.invalid_filename": "Nieprawidlowa nazwa pliku.",
        "pdf.invalid_pdf": "Przeslany plik nie jest poprawnym PDF.",
        "pdf.storage_error_file": "Blad zapisu na serwerze podczas przetwarzania pliku.",
        "pdf.split_success": "PDF zostal podzielony.",
        "pdf.no_files_uploaded": "Nie przeslano plikow.",
        "pdf.min_two_files": "Przeslij co najmniej dwa pliki PDF do scalenia.",
        "pdf.too_many_files": "Za duzo plikow. Maksymalnie {max_files} plikow.",
        "pdf.invalid_uploaded_filename": "Jeden z przeslanych plikow ma nieprawidlowa nazwe.",
        "pdf.single_file_too_large": "Jeden z plikow jest za duzy. Maksymalny rozmiar pliku to {size_mb} MB.",
        "pdf.total_upload_too_large": "Laczny rozmiar plikow jest za duzy. Maksimum to {size_mb} MB.",
        "pdf.invalid_pdf_in_set": "Co najmniej jeden z przeslanych plikow nie jest poprawnym PDF.",
        "pdf.storage_error_files": "Blad zapisu na serwerze podczas przetwarzania plikow.",
        "pdf.merge_success": "Pliki PDF zostaly scalone.",
        "pdf.extract_success": "Tekst z PDF zostal wyciagniety.",
    },
    "en": {
        "todo.description_required": "Task description is required.",
        "todo.task_added": "Task added.",
        "todo.task_deleted": "Task deleted.",
        "todo.task_updated": "Task updated.",
        "todo.invalid_task_id": "Invalid task ID.",
        "password.length_min": "Password length must be at least 4 characters.",
        "password.character_type_required": "Select at least one character type.",
        "password.length_integer": "Length must be an integer.",
        "password_strength.password_required": "Password is required.",
        "password_strength.score_0": "Very weak",
        "password_strength.score_1": "Weak",
        "password_strength.score_2": "Medium",
        "password_strength.score_3": "Strong",
        "password_strength.score_4": "Very strong",
        "password_strength.recommended_note": "For a typical web app, online attacks with rate limiting are usually the most realistic scenario.",
        "password_strength.scenario.online_throttled.label": "Online with rate limit",
        "password_strength.scenario.online_throttled.description": "Attack through login form with throttling and lockouts.",
        "password_strength.scenario.online_unthrottled.label": "Online without rate limit",
        "password_strength.scenario.online_unthrottled.description": "Online attack without effective request throttling.",
        "password_strength.scenario.offline_slow_hashing.label": "Offline, slow hashing",
        "password_strength.scenario.offline_slow_hashing.description": "Database leak and attack against expensive hash (bcrypt/argon2).",
        "password_strength.scenario.offline_fast_hashing.label": "Offline, fast hashing",
        "password_strength.scenario.offline_fast_hashing.description": "Database leak and GPU attack against fast hash.",
        "password_strength.unknown": "unknown",
        "pdf.no_file_uploaded": "No file uploaded.",
        "pdf.no_file_selected": "No file selected.",
        "pdf.only_pdf_allowed": "Only PDF files are allowed.",
        "pdf.file_too_large": "File is too large. Max size is {size_mb} MB.",
        "pdf.invalid_filename": "Invalid filename.",
        "pdf.invalid_pdf": "Uploaded file is not a valid PDF.",
        "pdf.storage_error_file": "Server storage error while processing file.",
        "pdf.split_success": "PDF split successfully.",
        "pdf.no_files_uploaded": "No files uploaded.",
        "pdf.min_two_files": "Upload at least two PDF files to merge.",
        "pdf.too_many_files": "Too many files. Max is {max_files} files.",
        "pdf.invalid_uploaded_filename": "One of the uploaded files has an invalid filename.",
        "pdf.single_file_too_large": "A file is too large. Max per file is {size_mb} MB.",
        "pdf.total_upload_too_large": "Total upload is too large. Max total is {size_mb} MB.",
        "pdf.invalid_pdf_in_set": "One or more uploaded files are not valid PDFs.",
        "pdf.storage_error_files": "Server storage error while processing files.",
        "pdf.merge_success": "PDF files merged successfully.",
        "pdf.extract_success": "Text extracted from PDF successfully.",
    },
}


def get_language():
    lang = request.headers.get("X-Language", "").strip().lower()
    if lang in SUPPORTED_LANGUAGES:
        return lang

    accept_language = request.headers.get("Accept-Language", "").lower()
    if accept_language.startswith("en"):
        return "en"
    return DEFAULT_LANGUAGE


def t(key, **kwargs):
    lang = get_language()
    text = TRANSLATIONS.get(lang, {}).get(key) or TRANSLATIONS[DEFAULT_LANGUAGE].get(key) or key
    if kwargs:
        return text.format(**kwargs)
    return text
