from dataclasses import dataclass


REQUIRED_METADATA = ("tooiCode", "documentType", "publishedAt", "sourceUrl")


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


@dataclass
class WooPreflightRequest:
    organisatie: str
    documentType: str


def check_woo_publicatieplicht(req: WooPreflightRequest, documents: list[dict]) -> dict:
    organisatie = _norm(req.organisatie)
    document_type = _norm(req.documentType)
    applied = ["WOO-001"]

    matches = [
        doc
        for doc in documents
        if doc.get("organisatie") == organisatie and doc.get("documentType") == document_type
    ]

    if not matches:
        return {
            "documentFound": False,
            "missingMetadata": list(REQUIRED_METADATA),
            "manualReviewRequired": True,
            "manualReviewReason": "Documenttype of organisatie niet gevonden in Woo-index/DiWoo fixture.",
            "appliedRules": ["WOO-001", "WOO-008"],
            "sourceRefs": [],
        }

    doc = matches[0]
    metadata = doc.get("metadata", {})
    missing = [field for field in REQUIRED_METADATA if not metadata.get(field)]
    applied.extend(["WOO-002", "WOO-003", "WOO-004"])

    if metadata.get("publishedAt"):
        applied.append("WOO-005")
    if metadata.get("sourceUrl"):
        applied.append("WOO-006")
    if missing:
        applied.append("WOO-007")

    return {
        "documentFound": True,
        "organisatie": doc.get("organisatieLabel"),
        "documentType": doc.get("documentTypeLabel"),
        "location": doc.get("location"),
        "missingMetadata": missing,
        "manualReviewRequired": bool(missing),
        "manualReviewReason": "Ontbrekende Woo/DiWoo metadata: " + ", ".join(missing) if missing else "",
        "appliedRules": list(dict.fromkeys(applied)),
        "sourceRefs": doc.get("sourceRefs", []),
    }
