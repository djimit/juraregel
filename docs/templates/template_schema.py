"""Template Schema & Validation — Fase 4: Tooling & Interoperabiliteit.

Garandeert consistente metadata voor alle templates:
- document (str): Naam van het document
- wettelijke_basis (str): Wettelijke verwijzing
- organisatie (str): Naam van de organisatie
- datum (str): ISO datum
- model_versie (str, optional): Versie van het model/bron
- bron (str, optional): Primaire bronvermelding
- inhoud (dict): Gestructureerde inhoud

Gebruik:
    from docs.templates.template_schema import validate_template, enrich_metadata
    doc = generate_document("dpia", "Gemeente Test", verwerking="WOZ")
    validated = validate_template(doc)  # raises on invalid
    enriched = enrich_metadata(doc, {"model_versie": "3.0", "bron": "KCBR"})
"""

from __future__ import annotations

from datetime import date
from typing import Any

REQUIRED_FIELDS = {"document", "wettelijke_basis", "organisatie", "datum", "inhoud"}
OPTIONAL_FIELDS = {"model_versie", "bron", "versie", "document_type", "language"}
ALL_FIELDS = REQUIRED_FIELDS | OPTIONAL_FIELDS


class TemplateValidationError(Exception):
    """Template voldoet niet aan het schema."""

    pass


def validate_template(doc: dict) -> dict:
    """Valideer dat een template-dict voldoet aan het schema.

    Returns:
        Het gevalideerde document (onveranderd)

    Raises:
        TemplateValidationError: Ontbrekende required fields of ongeldige types
    """
    if not isinstance(doc, dict):
        raise TemplateValidationError("Template moet een dict zijn")

    missing = REQUIRED_FIELDS - set(doc.keys())
    if missing:
        raise TemplateValidationError(
            f"Ontbrekende verplichte velden: {sorted(missing)}"
        )

    if not isinstance(doc["document"], str) or not doc["document"].strip():
        raise TemplateValidationError("'document' moet een niet-lege string zijn")

    if (
        not isinstance(doc["wettelijke_basis"], str)
        or not doc["wettelijke_basis"].strip()
    ):
        raise TemplateValidationError(
            "'wettelijke_basis' moet een niet-lege string zijn"
        )

    if not isinstance(doc["organisatie"], str):
        raise TemplateValidationError("'organisatie' moet een string zijn")

    if not isinstance(doc["inhoud"], dict):
        raise TemplateValidationError("'inhoud' moet een dict zijn")

    return doc


def enrich_metadata(doc: dict, overrides: dict | None = None) -> dict:
    """Verrijk een template met ontbrekende optionele metadata.

    Voegt automatisch toe als afwezig:
    - datum: vandaag (indien afwezig)
    - model_versie: "1.0" (indien afwezig)
    - language: "nl" (indien afwezig)
    """
    enriched = dict(doc)

    if "datum" not in enriched or not enriched["datum"]:
        enriched["datum"] = date.today().isoformat()

    if "model_versie" not in enriched or not enriched["model_versie"]:
        enriched["model_versie"] = "1.0"

    if "language" not in enriched:
        enriched["language"] = "nl"

    if overrides:
        for key, value in overrides.items():
            if key in ALL_FIELDS and value:
                enriched[key] = value

    return enriched


def get_template_info(doc: dict) -> dict:
    """Extract metadata-info uit een template."""
    return {
        "document": doc.get("document", "Onbekend"),
        "wettelijke_basis": doc.get("wettelijke_basis", "—"),
        "organisatie": doc.get("organisatie", "—"),
        "datum": doc.get("datum", "—"),
        "model_versie": doc.get("model_versie", "—"),
        "bron": doc.get("bron", "—"),
        "language": doc.get("language", "nl"),
        "section_count": _count_sections(doc.get("inhoud", {})),
        "has_checkboxes": _has_checkboxes(doc.get("inhoud", {})),
        "has_scoring": _has_scoring(doc.get("inhoud", {})),
    }


def _count_sections(inhoud: dict) -> int:
    """Tel het aantal secties in de inhoud."""
    return len(inhoud)


def _has_checkboxes(inhoud: Any) -> bool:
    """Check of de inhoud checkbox-items bevat."""
    text = str(inhoud)
    return "[ ]" in text or "[x]" in text or "[X]" in text


def _has_scoring(inhoud: Any) -> bool:
    """Check of de inhoud scoring bevat."""
    text = str(inhoud)
    return any(
        kw in text for kw in ["score", "scoring", "G1", "G2", "G3", "G4", "risico"]
    )


def list_template_capabilities(doc: dict) -> list[str]:
    """Lijst van capabilities gebaseerd op de template-structuur."""
    caps = []
    info = get_template_info(doc)

    if info["has_checkboxes"]:
        caps.append("interactive_checkboxes")
    if info["has_scoring"]:
        caps.append("risk_scoring")
    if info["section_count"] > 5:
        caps.append("multi_section")
    if "goedkeuring" in str(doc.get("inhoud", {})).lower():
        caps.append("approval_section")
    if "eindoordeel" in str(doc.get("inhoud", {})).lower():
        caps.append("conclusion_section")

    return caps
