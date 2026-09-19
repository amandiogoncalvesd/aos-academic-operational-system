"""i18n mínimo do core. Plugins podem registar catálogos adicionais."""
from contextvars import ContextVar

_locale: ContextVar[str] = ContextVar("locale", default="pt")

CATALOG: dict[str, dict[str, str]] = {
    "pt": {"welcome": "Bem-vindo ao AOS", "invalid_credentials": "Credenciais inválidas"},
    "en": {"welcome": "Welcome to AOS", "invalid_credentials": "Invalid credentials"},
    "umb": {"welcome": "Wakombelwa ku AOS"},
}


def set_locale(locale: str) -> None:
    _locale.set(locale if locale in CATALOG else "pt")


def get_locale() -> str:
    return _locale.get()


def translate_key(key: str, locale: str | None = None, **kwargs) -> str:
    loc = locale or get_locale()
    text = CATALOG.get(loc, {}).get(key) or CATALOG["pt"].get(key) or key
    return text.format(**kwargs) if kwargs else text


_ = translate_key
