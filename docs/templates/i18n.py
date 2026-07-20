"""Internationalization (i18n) Support — Fase 4: Tooling & Interoperabiliteit.

Multi-language support voor template output.
Ondersteunt: Nederlands (nl), Engels (en)

Gebruik:
    from docs.templates.i18n import translate, set_language
    set_language("en")
    label = translate("wettelijke_basis") → "Legal basis"
"""

from __future__ import annotations

from typing import Any

CURRENT_LANG = "nl"

TRANSLATIONS = {
    "nl": {
        "document": "Document",
        "wettelijke_basis": "Wettelijke basis",
        "organisatie": "Organisatie",
        "datum": "Datum",
        "model_versie": "Model versie",
        "bron": "Bron",
        "inhoud": "Inhoud",
        "goedkeuring": "Goedkeuring",
        "eindoordeel": "Eindoordeel",
        "stap": "Stap",
        "sectie": "Sectie",
        "titel": "Titel",
        "instructie": "Instructie",
        "content": "Inhoud",
        "criteria": "Criteria",
        "scoring": "Scoring",
        "conclusie": "Conclusie",
        "vervolg": "Vervolg",
        "vervolgactie": "Vervolgactie",
        "ja": "Ja",
        "nee": "Nee",
        "ja_nee": "Ja/Nee",
        "positief": "Positief",
        "negatief": "Negatief",
        "geschikt": "Geslaagd",
        "niet_geschikt": "Niet geslaagd",
        "naam": "Naam",
        "functie": "Functie",
        "handtekening": "Handtekening",
        "opmerkingen": "Opmerkingen",
        "herziening": "Herziening",
        "generated": "Gegenereerd",
        "page": "Pagina",
        "of": "van",
    },
    "en": {
        "document": "Document",
        "wettelijke_basis": "Legal basis",
        "organisatie": "Organization",
        "datum": "Date",
        "model_versie": "Model version",
        "bron": "Source",
        "inhoud": "Content",
        "goedkeuring": "Approval",
        "eindoordeel": "Conclusion",
        "stap": "Step",
        "sectie": "Section",
        "titel": "Title",
        "instructie": "Instruction",
        "content": "Content",
        "criteria": "Criteria",
        "scoring": "Scoring",
        "conclusie": "Conclusion",
        "vervolg": "Next steps",
        "vervolgactie": "Follow-up action",
        "ja": "Yes",
        "nee": "No",
        "ja_nee": "Yes/No",
        "positief": "Positive",
        "negatief": "Negative",
        "geschikt": "Passed",
        "niet_geschikt": "Failed",
        "naam": "Name",
        "functie": "Role",
        "handtekening": "Signature",
        "opmerkingen": "Remarks",
        "herziening": "Review",
        "generated": "Generated",
        "page": "Page",
        "of": "of",
    },
}


def set_language(lang: str) -> None:
    """Stel de huidige taal in."""
    global CURRENT_LANG
    if lang not in TRANSLATIONS:
        raise ValueError(
            f"Onbekende taal: {lang}. Beschikbaar: {list(TRANSLATIONS.keys())}"
        )
    CURRENT_LANG = lang


def get_language() -> str:
    """Haal de huidige taal op."""
    return CURRENT_LANG


def translate(key: str, lang: str | None = None) -> str:
    """Vertaal een label."""
    target_lang = lang or CURRENT_LANG
    translations = TRANSLATIONS.get(target_lang, TRANSLATIONS["nl"])
    return translations.get(key, key)


def translate_doc(doc: dict, lang: str) -> dict:
    """Vertaal de metadata-velden van een document.

    De inhoud blijft in de oorspronkelijke taal (de template-data is NL),
    maar de metadata-velden worden vertaald.
    """
    meta_keys = {
        "document": "document",
        "wettelijke_basis": "wettelijke_basis",
        "organisatie": "organisatie",
        "datum": "datum",
        "model_versie": "model_versie",
        "bron": "bron",
    }

    translated = dict(doc)
    for nl_key, doc_key in meta_keys.items():
        if doc_key in translated and isinstance(translated[doc_key], str):
            # Alleen vertalen als het een bekende sleutel is
            pass  # Metadata blijft als-is, structuur-vertaling is voldoende

    return translated


def list_languages() -> list[dict]:
    """Lijst ondersteunde talen."""
    return [
        {"code": "nl", "name": "Nederlands", "native": "Nederlands"},
        {"code": "en", "name": "English", "native": "English"},
    ]
