import difflib
import re

from flask import Blueprint, jsonify, request

from extensions import limiter
from i18n import t

text_diff_bp = Blueprint("text_diff_api", __name__)


def build_stats(seq_a, seq_b):
    matcher = difflib.SequenceMatcher(a=seq_a, b=seq_b)
    added = 0
    missing = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in {"replace", "delete"}:
            missing += i2 - i1
        if tag in {"replace", "insert"}:
            added += j2 - j1

    return {
        "similarity_percent": round(matcher.ratio() * 100, 2),
        "added_count": added,
        "missing_count": missing,
        "is_identical": added == 0 and missing == 0,
    }


def join_tokens(tokens, mode):
    if mode == "line":
        return "\n".join(tokens)
    if mode == "word":
        return " ".join(tokens)
    return "".join(tokens)


def build_diff_entries(seq_a, seq_b, mode):
    matcher = difflib.SequenceMatcher(a=seq_a, b=seq_b)
    entries = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in {"replace", "delete"}:
            text = join_tokens(seq_a[i1:i2], mode).strip()
            if text:
                entries.append({"type": "missing", "text": text})
        if tag in {"replace", "insert"}:
            text = join_tokens(seq_b[j1:j2], mode).strip()
            if text:
                entries.append({"type": "added", "text": text})

    return entries


def normalize_text(text, ignore_whitespace, ignore_case):
    value = text
    if ignore_case:
        value = value.casefold()
    if ignore_whitespace:
        value = re.sub(r"\s+", " ", value).strip()
    return value


def tokenize_text(text, mode):
    if mode == "char":
        return list(text)
    if mode == "word":
        return re.findall(r"\S+", text)
    return text.splitlines()


@text_diff_bp.route("/api/text_diff", methods=["POST"])
@limiter.limit("120 per minute")
def text_diff_api():
    data = request.json or {}
    text_a = data.get("text_a", "")
    text_b = data.get("text_b", "")
    ignore_whitespace = bool(data.get("ignore_whitespace", False))
    ignore_case = bool(data.get("ignore_case", False))
    compare_mode = (data.get("compare_mode", "word") or "word").lower()
    if compare_mode not in {"line", "word", "char"}:
        compare_mode = "word"

    if not isinstance(text_a, str) or not isinstance(text_b, str):
        return jsonify({"error": t("text_diff.invalid_input")}), 400

    normalized_a = normalize_text(text_a, ignore_whitespace, ignore_case)
    normalized_b = normalize_text(text_b, ignore_whitespace, ignore_case)
    seq_a = tokenize_text(normalized_a, compare_mode)
    seq_b = tokenize_text(normalized_b, compare_mode)
    stats = build_stats(seq_a, seq_b)
    diff_entries = []
    if stats["is_identical"] and (text_a != text_b):
        diff_text = t("text_diff.no_changes_with_options")
    elif stats["is_identical"]:
        diff_text = t("text_diff.no_changes")
    else:
        diff_entries = build_diff_entries(seq_a, seq_b, compare_mode)
        diff_text = ""

    return jsonify(
        {
            "message": t("text_diff.success"),
            "stats": stats,
            "diff_text": diff_text,
            "diff_entries": diff_entries,
            "options": {
                "ignore_whitespace": ignore_whitespace,
                "ignore_case": ignore_case,
                "compare_mode": compare_mode,
            },
        }
    )
