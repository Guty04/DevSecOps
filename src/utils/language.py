from functools import lru_cache
from gettext import NullTranslations, translation

from src.constants import TRANSLATES_DIR


@lru_cache
def get_translation(language: str) -> NullTranslations:
    return translation(domain="messages", localedir=TRANSLATES_DIR, languages=[language], fallback=True)


def get_translate(language: str, message: str) -> str:
    translation: NullTranslations = get_translation(language)

    return translation.gettext(message)
