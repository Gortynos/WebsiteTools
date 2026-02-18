import secrets
import string

from flask import Blueprint, jsonify, request
from extensions import limiter
from i18n import get_language, t
from zxcvbn import zxcvbn

password_bp = Blueprint("password_api", __name__)


def generate_password(length, include_uppercase, include_special, include_digits):
    if length < 4:
        return {"error": t("password.length_min")}

    lower = string.ascii_lowercase
    uppercase = string.ascii_uppercase if include_uppercase else ""
    special = string.punctuation if include_special else ""
    digits = string.digits if include_digits else ""
    all_characters = lower + uppercase + special + digits

    if not all_characters:
        return {"error": t("password.character_type_required")}

    required_characters = []
    if include_uppercase:
        required_characters.append(secrets.choice(uppercase))
    if include_special:
        required_characters.append(secrets.choice(special))
    if include_digits:
        required_characters.append(secrets.choice(digits))

    remaining_length = length - len(required_characters)
    password = required_characters + [secrets.choice(all_characters) for _ in range(remaining_length)]

    # Crypto-safe in-place shuffle using Fisher-Yates.
    for i in range(len(password) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        password[i], password[j] = password[j], password[i]

    return {"password": "".join(password)}


def format_duration(seconds):
    if seconds is None:
        return t("password_strength.unknown")

    try:
        value = float(seconds)
    except (TypeError, ValueError):
        return t("password_strength.unknown")

    lang = get_language()

    def plural_pl(number, forms):
        if number == 1:
            return forms[0]
        if number % 10 in {2, 3, 4} and number % 100 not in {12, 13, 14}:
            return forms[1]
        return forms[2]

    if value < 1:
        return "< 1 sekunda" if lang == "pl" else "< 1 second"

    if value < 60:
        amount = int(value)
        if lang == "pl":
            return f"{amount} {plural_pl(amount, ('sekunda', 'sekundy', 'sekund'))}"
        return f"{amount} second" if amount == 1 else f"{amount} seconds"

    if value < 3600:
        amount = int(value // 60)
        if lang == "pl":
            return f"{amount} {plural_pl(amount, ('minuta', 'minuty', 'minut'))}"
        return f"{amount} minute" if amount == 1 else f"{amount} minutes"

    if value < 86400:
        amount = int(value // 3600)
        if lang == "pl":
            return f"{amount} {plural_pl(amount, ('godzina', 'godziny', 'godzin'))}"
        return f"{amount} hour" if amount == 1 else f"{amount} hours"

    if value < 31536000:
        amount = int(value // 86400)
        if lang == "pl":
            return f"{amount} {plural_pl(amount, ('dzień', 'dni', 'dni'))}"
        return f"{amount} day" if amount == 1 else f"{amount} days"

    amount = int(value // 31536000)
    if lang == "pl":
        return f"{amount} {plural_pl(amount, ('rok', 'lata', 'lat'))}"
    return f"{amount} year" if amount == 1 else f"{amount} years"


def translate_feedback_text(text):
    if not text or get_language() != "pl":
        return text or ""

    translations = {
        "This is similar to a commonly used password.": "To hasło jest podobne do często używanego hasła.",
        "This is a top-10 common password.": "To hasło jest w TOP-10 najczęściej używanych haseł.",
        "This is a top-100 common password.": "To hasło jest w TOP-100 najczęściej używanych haseł.",
        "This is a very common password.": "To bardzo często używane hasło.",
        "A word by itself is easy to guess.": "Pojedyncze słowo jest łatwe do odgadnięcia.",
        "Names and surnames by themselves are easy to guess.": "Same imiona i nazwiska są łatwe do odgadnięcia.",
        "Common names and surnames are easy to guess.": "Popularne imiona i nazwiska są łatwe do odgadnięcia.",
        "Straight rows of keys are easy to guess.": "Proste układy klawiszy są łatwe do odgadnięcia.",
        "Short keyboard patterns are easy to guess.": "Krótkie wzorce klawiaturowe są łatwe do odgadnięcia.",
        "Repeats like \"aaa\" are easy to guess.": "Powtórzenia typu \"aaa\" są łatwe do odgadnięcia.",
        "Repeats like \"abcabcabc\" are only slightly harder to guess than \"abc\".": "Powtórzenia typu \"abcabcabc\" są tylko trochę trudniejsze niż \"abc\".",
        "Sequences like abc or 6543 are easy to guess.": "Sekwencje typu abc albo 6543 są łatwe do odgadnięcia.",
        "Recent years are easy to guess.": "Nowsze lata są łatwe do odgadnięcia.",
        "Dates are often easy to guess.": "Daty często są łatwe do odgadnięcia.",
        "Add another word or two. Uncommon words are better.": "Dodaj jedno lub dwa dodatkowe słowa. Rzadziej używane słowa są lepsze.",
        "Avoid repeated words and characters.": "Unikaj powtarzania słów i znaków.",
        "Avoid sequences.": "Unikaj sekwencji.",
        "Avoid recent years.": "Unikaj nowszych lat.",
        "Avoid years that are associated with you.": "Unikaj lat, które są z Tobą powiązane.",
        "Avoid dates and years that are associated with you.": "Unikaj dat i lat, które są z Tobą powiązane.",
        "Capitalization doesn't help very much.": "Użycie wielkich liter niewiele pomaga.",
        "All-uppercase is almost as easy to guess as all-lowercase.": "Wszystkie wielkie litery są prawie tak samo łatwe do odgadnięcia jak małe.",
        "Reversed words aren't much harder to guess.": "Odwrócone słowa nie są dużo trudniejsze do odgadnięcia.",
        "Predictable substitutions like '@' instead of 'a' don't help very much.": "Przewidywalne zamiany, np. '@' zamiast 'a', niewiele pomagają.",
    }
    return translations.get(text, text)


def build_crack_time_scenarios(crack_seconds):
    scenarios = [
        {
            "key": "online_throttled",
            "seconds": crack_seconds.get("online_throttling_100_per_hour"),
            "label": t("password_strength.scenario.online_throttled.label"),
            "description": t("password_strength.scenario.online_throttled.description"),
        },
        {
            "key": "online_unthrottled",
            "seconds": crack_seconds.get("online_no_throttling_10_per_second"),
            "label": t("password_strength.scenario.online_unthrottled.label"),
            "description": t("password_strength.scenario.online_unthrottled.description"),
        },
        {
            "key": "offline_slow_hashing",
            "seconds": crack_seconds.get("offline_slow_hashing_1e4_per_second"),
            "label": t("password_strength.scenario.offline_slow_hashing.label"),
            "description": t("password_strength.scenario.offline_slow_hashing.description"),
        },
        {
            "key": "offline_fast_hashing",
            "seconds": crack_seconds.get("offline_fast_hashing_1e10_per_second"),
            "label": t("password_strength.scenario.offline_fast_hashing.label"),
            "description": t("password_strength.scenario.offline_fast_hashing.description"),
        },
    ]
    recommended_key = "online_throttled"

    return {
        "recommended_key": recommended_key,
        "recommended_note": t("password_strength.recommended_note"),
        "scenarios": [
            {
                "key": item["key"],
                "label": item["label"],
                "description": item["description"],
                "time": format_duration(item["seconds"]),
                "is_recommended": item["key"] == recommended_key,
            }
            for item in scenarios
        ],
    }


@password_bp.route("/api/generate_password", methods=["POST"])
@limiter.limit("30 per minute")
def generate_password_api():
    data = request.json or {}
    try:
        length = int(data.get("length", 8))
    except (TypeError, ValueError):
        return jsonify({"error": t("password.length_integer")}), 400

    include_uppercase = data.get("include_uppercase", False)
    include_special = data.get("include_special", False)
    include_digits = data.get("include_digits", False)

    result = generate_password(length, include_uppercase, include_special, include_digits)
    return jsonify(result)


@password_bp.route("/api/password_strength", methods=["POST"])
@limiter.limit("60 per minute")
def password_strength_api():
    data = request.json or {}
    password = data.get("password", "")
    if not password:
        return jsonify({"error": t("password_strength.password_required")}), 400

    analysis = zxcvbn(password)
    crack_seconds = analysis.get("crack_times_seconds", {})
    feedback = analysis.get("feedback", {})
    score = int(analysis.get("score", 0))

    result = {
        "score": score,
        "score_label": t(f"password_strength.score_{score}"),
        "guesses_log10": analysis.get("guesses_log10"),
        "crack_time": build_crack_time_scenarios(crack_seconds),
        "feedback": {
            "warning": translate_feedback_text(feedback.get("warning") or ""),
            "suggestions": [translate_feedback_text(item) for item in (feedback.get("suggestions") or [])],
        },
    }
    return jsonify(result)
