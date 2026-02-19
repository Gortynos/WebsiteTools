# WebsiteTools

Web application with a set of practical productivity and document tools, built with Flask.

## Live Features

- To-Do List (CRUD, local JSON persistence)
- Password Generator (secure randomness via `secrets`)
- Password Strength Checker (`zxcvbn` + readable crack-time scenarios)
- PDF Split
- PDF Merge
- PDF Text Extract (plain text / JSON)
- Text Comparison (line / word / char modes, readable diff output)
- PL/EN language switch
- Responsive UI with top navigation

## Tech Stack

- Backend: Python, Flask, Flask Blueprints
- Security / reliability: Flask-Limiter, input validation, structured error handling
- PDF processing: PyMuPDF (`fitz`)
- Password strength estimation: `zxcvbn`
- Frontend: HTML, CSS, vanilla JavaScript

## Run Locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

## Configuration

Environment variables used by the app:

- `FLASK_DEBUG` (`0/1`, `true/false`)
- `LOG_LEVEL` (default: `INFO`)
- `MAX_PDF_SIZE_MB` (default: `10`)
- `MAX_MERGE_TOTAL_PDF_SIZE_MB` (default: `30`)
- `MAX_MERGE_FILES` (default: `20`)
- `RATELIMIT_STORAGE_URI` (default: `memory://`)

## Deploy Notes (Cyber_Folks / Passenger)

If app is hosted under a subpath (e.g. `/WebsiteTools`), make sure your `passenger_wsgi.py` points to the correct project directory and exports `application`.

Minimal example:

```python
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "WebsiteTools")  # adjust if needed

if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

from app import create_app
application = create_app()
```

## Project Structure

```text
WebsiteTools/
  app.py
  requirements.txt
  passenger_wsgi.py
  blueprints/
    pages.py
    todo.py
    password.py
    pdf.py
    text_diff.py
  templates/
  static/
```

## Why This Project

This project was developed as a practical toolkit and a portfolio piece focused on:

- clean Flask modularization (Blueprints),
- production-minded defaults (rate limiting, safer password generation, upload validation),
- clear UX and bilingual interface.

