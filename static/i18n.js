const TRANSLATIONS = {
    pl: {
        "common.toggle_label": "EN",
        "common.back": "Powrót",
        "home.title": "Moje narzędzia",
        "home.h1": "Witaj w moich aplikacjach!",
        "home.subtitle": "Wybierz aplikację, którą chcesz uruchomić:",
        "home.todo": "Lista zadań",
        "home.todo_desc": "Prosty manager zadań z zapisem lokalnym.",
        "home.password": "Generator haseł",
        "home.password_desc": "Generowanie losowych haseł z wybranymi regułami.",
        "home.password_strength": "Ocena siły hasła",
        "home.password_strength_desc": "Ocena bezpieczeństwa hasła i scenariusze łamania.",
        "home.pdf": "Podziel/Scal PDF",
        "home.pdf_desc": "Dzielenie PDF na strony oraz scalanie plików.",
        "home.pdf_extract": "Wyciąganie tekstu z PDF",
        "home.pdf_extract_desc": "Ekstrakcja treści z PDF do tekstu lub JSON.",
        "home.text_diff": "Porównanie tekstów (A/B)",
        "home.text_diff_desc": "Czytelne porównanie różnic między dwiema wersjami tekstu.",
        "home.view_label": "Widok",
        "home.view_cards": "Kafelki",
        "home.view_list": "Lista",
        "appearance.title": "Motyw",
        "appearance.preset_slate": "Niebiesko-szary",
        "appearance.preset_sand": "Beżowo-błękitny",
        "appearance.preset_cyan": "Cyjan nocny",
        "menu.home": "Start",
        "menu.todo": "Lista zadań",
        "menu.password": "Generator haseł",
        "menu.password_strength": "Ocena siły hasła",
        "menu.pdf": "Podziel/Scal PDF",
        "menu.pdf_extract": "Tekst z PDF",
        "menu.text_diff": "Porównanie tekstów",
        "todo.title": "Lista zadań",
        "todo.h1": "Lista zadań",
        "todo.placeholder": "Wpisz zadanie",
        "todo.add": "Dodaj zadanie",
        "todo.status_completed": "[Zakończone]",
        "todo.status_not_completed": "[Niezakończone]",
        "todo.created_at": "Dodano",
        "todo.empty_alert": "Wpisz zadanie!",
        "password.title": "Generator haseł",
        "password.h1": "Generator haseł",
        "password.length": "Długość hasła:",
        "password.uppercase": "Uwzględnij wielkie litery",
        "password.special": "Uwzględnij znaki specjalne",
        "password.digits": "Uwzględnij cyfry",
        "password.generate": "Generuj hasło",
        "password.result": "Wygenerowane hasło:",
        "password_strength.title": "Ocena siły hasła",
        "password_strength.h1": "Ocena siły hasła",
        "password_strength.privacy_notice": "Hasło nie jest nigdzie zapisywane. Analiza jest wykonywana tylko na potrzeby bieżącego wyniku.",
        "password_strength.password_label": "Hasło:",
        "password_strength.show_password": "Pokaż",
        "password_strength.hide_password": "Ukryj",
        "password_strength.result_title": "Wynik:",
        "password_strength.crack_time_title": "Szacowany czas łamania (różne scenariusze):",
        "password_strength.recommended_badge": "Najbardziej realistyczny",
        "password_strength.waiting_input": "Wpisz hasło, aby zobaczyć analizę.",
        "password_strength.live_status": "Analiza zaktualizowana na podstawie wpisanego hasła.",
        "password_strength.error_status": "Nie udało się wykonać analizy.",
        "password_strength.score_label": "Ocena",
        "password_strength.warning_label": "Ostrzeżenie",
        "password_strength.error_prefix": "Błąd:",
        "password_strength.unknown_error": "Nieznany błąd",
        "pdf.title": "Podziel/Scal PDF",
        "pdf_extract.title": "Wyciąganie tekstu z PDF",
        "pdf_extract.h1": "Wyciągnij tekst z PDF",
        "pdf.split_h1": "Podziel PDF",
        "pdf.split_button": "Wgraj i podziel",
        "pdf.split_files": "Podzielone pliki:",
        "pdf.merge_h1": "Scal PDF",
        "pdf.merge_button": "Wgraj i scal",
        "pdf.merged_file": "Scalony plik:",
        "pdf.extract_h1": "Wyciągnij tekst z PDF",
        "pdf.extract_button": "Wgraj i wyciągnij tekst",
        "pdf.output_format_label": "Format wyjścia:",
        "pdf.output_text": "Plain text",
        "pdf.output_json": "JSON",
        "pdf.extract_result": "Wynik ekstrakcji:",
        "pdf.pick_extract_file_alert": "Wybierz plik PDF do ekstrakcji tekstu!",
        "pdf.pick_file_alert": "Wybierz plik!",
        "pdf.pick_two_files_alert": "Wybierz co najmniej dwa pliki PDF!",
        "pdf.error_prefix": "Błąd:",
        "text_diff.title": "Porównanie tekstów (A/B)",
        "text_diff.h1": "Porównanie tekstów (A/B)",
        "text_diff.input_a": "Tekst A",
        "text_diff.input_b": "Tekst B",
        "text_diff.ignore_whitespace": "Ignoruj białe znaki",
        "text_diff.ignore_case": "Ignoruj wielkość liter",
        "text_diff.pair_groups": "Grupuj różnice parami",
        "text_diff.compare_mode_label": "Tryb porównania:",
        "text_diff.compare_mode_line": "Linie",
        "text_diff.compare_mode_word": "Wyrazy",
        "text_diff.compare_mode_char": "Znaki",
        "text_diff.compare_button": "Porównaj",
        "text_diff.summary_title": "Podsumowanie",
        "text_diff.diff_title": "Różnice",
        "text_diff.similarity": "Podobieństwo",
        "text_diff.added_items": "Dodane elementy",
        "text_diff.missing_items": "Brakujące elementy",
        "text_diff.added_prefix": "Dodane",
        "text_diff.missing_prefix": "Brakuje",
        "text_diff.error_prefix": "Błąd:",
        "text_diff.unknown_error": "Nieznany błąd",
    },
    en: {
        "common.toggle_label": "PL",
        "common.back": "Back",
        "home.title": "My tools",
        "home.h1": "Welcome to my applications!",
        "home.subtitle": "Choose an application to run:",
        "home.todo": "To-Do List",
        "home.todo_desc": "Simple task manager with local persistence.",
        "home.password": "Password Generator",
        "home.password_desc": "Generate random passwords with selected rules.",
        "home.password_strength": "Password Strength Checker",
        "home.password_strength_desc": "Evaluate password security and crack-time scenarios.",
        "home.pdf": "Split/Merge PDF",
        "home.pdf_desc": "Split PDF pages and merge multiple files.",
        "home.pdf_extract": "PDF Text Extract",
        "home.pdf_extract_desc": "Extract PDF content to plain text or JSON.",
        "home.text_diff": "Text Comparison (A/B)",
        "home.text_diff_desc": "Readable comparison between two text versions.",
        "home.view_label": "View",
        "home.view_cards": "Cards",
        "home.view_list": "List",
        "appearance.title": "Theme",
        "appearance.preset_slate": "Blue-gray",
        "appearance.preset_sand": "Beige-blue",
        "appearance.preset_cyan": "Cyan night",
        "menu.home": "Home",
        "menu.todo": "To-Do",
        "menu.password": "Generator",
        "menu.password_strength": "Strength",
        "menu.pdf": "PDF Split/Merge",
        "menu.pdf_extract": "PDF Text",
        "menu.text_diff": "Text Compare",
        "todo.title": "To-Do List",
        "todo.h1": "To-Do List",
        "todo.placeholder": "Enter a task",
        "todo.add": "Add task",
        "todo.status_completed": "[Completed]",
        "todo.status_not_completed": "[Not completed]",
        "todo.created_at": "Created",
        "todo.empty_alert": "Enter a task!",
        "password.title": "Password Generator",
        "password.h1": "Password Generator",
        "password.length": "Password length:",
        "password.uppercase": "Include uppercase",
        "password.special": "Include special characters",
        "password.digits": "Include digits",
        "password.generate": "Generate password",
        "password.result": "Generated password:",
        "password_strength.title": "Password Strength Checker",
        "password_strength.h1": "Password Strength Checker",
        "password_strength.privacy_notice": "Your password is not stored anywhere. Analysis is performed only for the current result.",
        "password_strength.password_label": "Password:",
        "password_strength.show_password": "Show",
        "password_strength.hide_password": "Hide",
        "password_strength.result_title": "Result:",
        "password_strength.crack_time_title": "Estimated crack time (different scenarios):",
        "password_strength.recommended_badge": "Most realistic",
        "password_strength.waiting_input": "Type a password to see analysis.",
        "password_strength.live_status": "Analysis updated from your typed password.",
        "password_strength.error_status": "Analysis failed.",
        "password_strength.score_label": "Score",
        "password_strength.warning_label": "Warning",
        "password_strength.error_prefix": "Error:",
        "password_strength.unknown_error": "Unknown error",
        "pdf.title": "Split/Merge PDF",
        "pdf_extract.title": "PDF Text Extract",
        "pdf_extract.h1": "Extract text from PDF",
        "pdf.split_h1": "Split PDF",
        "pdf.split_button": "Upload and split",
        "pdf.split_files": "Split files:",
        "pdf.merge_h1": "Merge PDF",
        "pdf.merge_button": "Upload and merge",
        "pdf.merged_file": "Merged file:",
        "pdf.extract_h1": "Extract text from PDF",
        "pdf.extract_button": "Upload and extract text",
        "pdf.output_format_label": "Output format:",
        "pdf.output_text": "Plain text",
        "pdf.output_json": "JSON",
        "pdf.extract_result": "Extraction result:",
        "pdf.pick_extract_file_alert": "Please select a PDF file for text extraction!",
        "pdf.pick_file_alert": "Please select a file!",
        "pdf.pick_two_files_alert": "Please select at least two PDF files!",
        "pdf.error_prefix": "Error:",
        "text_diff.title": "Text Comparison (A/B)",
        "text_diff.h1": "Text Comparison (A/B)",
        "text_diff.input_a": "Text A",
        "text_diff.input_b": "Text B",
        "text_diff.ignore_whitespace": "Ignore whitespace",
        "text_diff.ignore_case": "Ignore letter case",
        "text_diff.pair_groups": "Group differences in pairs",
        "text_diff.compare_mode_label": "Compare mode:",
        "text_diff.compare_mode_line": "Lines",
        "text_diff.compare_mode_word": "Words",
        "text_diff.compare_mode_char": "Characters",
        "text_diff.compare_button": "Compare",
        "text_diff.summary_title": "Summary",
        "text_diff.diff_title": "Diff",
        "text_diff.similarity": "Similarity",
        "text_diff.added_items": "Added items",
        "text_diff.missing_items": "Missing items",
        "text_diff.added_prefix": "Added",
        "text_diff.missing_prefix": "Missing",
        "text_diff.error_prefix": "Error:",
        "text_diff.unknown_error": "Unknown error",
    },
};

function getCurrentLanguage() {
    const saved = localStorage.getItem("lang");
    if (saved === "pl" || saved === "en") {
        return saved;
    }
    return "pl";
}

function setCurrentLanguage(lang) {
    if (lang !== "pl" && lang !== "en") {
        return;
    }
    localStorage.setItem("lang", lang);
}

function t(key) {
    const lang = getCurrentLanguage();
    return (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) || key;
}

const PAGE_PATHS = [
    "todo",
    "password",
    "password-strength",
    "split-pdf",
    "extract-pdf-text",
    "text-diff",
];

function getAppBasePath() {
    const parts = window.location.pathname.split("/").filter(Boolean);
    if (parts.length === 0) {
        return "";
    }
    const last = parts[parts.length - 1];
    if (PAGE_PATHS.includes(last)) {
        return `/${parts.slice(0, -1).join("/")}`;
    }
    return `/${parts.join("/")}`;
}

function buildAppUrl(path = "") {
    const base = getAppBasePath();
    const cleanPath = String(path || "").replace(/^\/+|\/+$/g, "");
    if (!cleanPath) {
        return `${base || ""}/`;
    }
    return `${base || ""}/${cleanPath}`;
}

function applyTranslations() {
    const lang = getCurrentLanguage();
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-i18n]").forEach((element) => {
        const key = element.getAttribute("data-i18n");
        element.textContent = t(key);
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
        const key = element.getAttribute("data-i18n-placeholder");
        element.placeholder = t(key);
    });

    const badge = document.getElementById("languageBadge");
    if (badge) {
        badge.textContent = lang.toUpperCase();
    }
}

function toggleLanguage() {
    const current = getCurrentLanguage();
    const next = current === "pl" ? "en" : "pl";
    setCurrentLanguage(next);
    applyTranslations();

    if (typeof window.onLanguageChange === "function") {
        window.onLanguageChange(next);
    }
}

function createLanguageToggle() {
    const wrapper = document.createElement("div");
    wrapper.className = "language-controls";

    const badge = document.createElement("span");
    badge.id = "languageBadge";
    badge.className = "language-badge";
    wrapper.appendChild(badge);

    const button = document.createElement("button");
    button.className = "language-toggle";
    button.type = "button";
    button.setAttribute("data-i18n", "common.toggle_label");
    button.addEventListener("click", toggleLanguage);
    wrapper.appendChild(button);

    const host = document.getElementById("topMenuRight") || document.body;
    host.appendChild(wrapper);
}

function createTopMenu() {
    if (document.getElementById("topMenu")) {
        return;
    }

    const nav = document.createElement("nav");
    nav.id = "topMenu";
    nav.className = "top-menu";

    const brand = document.createElement("a");
    brand.className = "top-menu-brand";
    brand.href = buildAppUrl();
    brand.textContent = "WebsiteTools";
    nav.appendChild(brand);

    const links = document.createElement("div");
    links.className = "top-menu-links";
    const items = [
        { href: "", key: "menu.home" },
        { href: "todo", key: "menu.todo" },
        { href: "password", key: "menu.password" },
        { href: "password-strength", key: "menu.password_strength" },
        { href: "split-pdf", key: "menu.pdf" },
        { href: "extract-pdf-text", key: "menu.pdf_extract" },
        { href: "text-diff", key: "menu.text_diff" },
    ];

    const currentPath = window.location.pathname.replace(/\/$/, "") || "/";
    items.forEach((item) => {
        const link = document.createElement("a");
        link.href = buildAppUrl(item.href);
        link.setAttribute("data-i18n", item.key);
        link.textContent = t(item.key);
        const normalized = new URL(link.href, window.location.origin).pathname.replace(/\/$/, "") || "/";
        if (normalized === currentPath) {
            link.classList.add("active");
        }
        links.appendChild(link);
    });
    nav.appendChild(links);

    const right = document.createElement("div");
    right.id = "topMenuRight";
    right.className = "top-menu-right";
    nav.appendChild(right);

    document.body.prepend(nav);
}

function applyUiPreset(preset) {
    document.body.setAttribute("data-ui-preset", "sand-blue");
    localStorage.setItem("uiPreset", "sand-blue");
}

function wrapPageContent() {
    if (document.body.classList.contains("home-page")) {
        return;
    }
    if (document.querySelector("main.tool-shell")) {
        return;
    }

    const shell = document.createElement("main");
    shell.className = "tool-shell";
    const children = Array.from(document.body.childNodes);
    children.forEach((node) => {
        shell.appendChild(node);
    });
    document.body.appendChild(shell);
}

async function apiFetch(url, options = {}) {
    const headers = new Headers(options.headers || {});
    headers.set("X-Language", getCurrentLanguage());
    const finalUrl = /^https?:\/\//i.test(url) ? url : buildAppUrl(url);
    return fetch(finalUrl, { ...options, headers });
}

window.I18n = {
    t,
    getCurrentLanguage,
    setCurrentLanguage,
    applyTranslations,
    createLanguageToggle,
    apiFetch,
};

document.addEventListener("DOMContentLoaded", () => {
    applyUiPreset();
    wrapPageContent();
    createTopMenu();
    createLanguageToggle();
    applyTranslations();
});
