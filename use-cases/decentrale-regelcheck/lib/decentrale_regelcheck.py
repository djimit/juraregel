from dataclasses import dataclass


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


def _postcode(value: str) -> str:
    return _norm(value).replace(" ", "")


@dataclass
class DecentraleRegelcheckRequest:
    postcode: str
    product: str
    activiteit: str = ""
    bestuurslaag: str = ""


def check_decentrale_regel(req: DecentraleRegelcheckRequest, records: list[dict]) -> dict:
    postcode = _postcode(req.postcode)
    product = _norm(req.product)
    activiteit = _norm(req.activiteit)
    bestuurslaag = _norm(req.bestuurslaag)

    applied = ["DRC-001"]
    reasons = []
    matches = [
        record
        for record in records
        if record.get("postcode") == postcode
        and (record.get("product") == product or (activiteit and record.get("activiteit") == activiteit))
    ]

    if bestuurslaag:
        applied.append("DRC-003")
        matches = [record for record in matches if record.get("bestuurslaag") == bestuurslaag]

    if not matches:
        return {
            "matches": [],
            "bevoegdGezag": None,
            "procedureType": None,
            "manualReviewRequired": True,
            "manualReviewReason": "Geen lokale regeling gevonden voor postcode/product/activiteit.",
            "appliedRules": ["DRC-001", "DRC-009"],
            "sourceRefs": [],
        }

    applied.extend(["DRC-002", "DRC-004", "DRC-005"])
    source_refs = []
    manual = False
    for match in matches:
        source_refs.extend(match.get("sourceRefs", []))
        if match.get("openNormen"):
            manual = True
            applied.append("DRC-006")
            reasons.append("Open normen: " + ", ".join(match["openNormen"]))

    if len(matches) > 1:
        applied.append("DRC-007")
        manual = True
        reasons.append("Meerdere bevoegde gezagen of regelingen gevonden.")

    primary = matches[0]
    return {
        "matches": matches,
        "bevoegdGezag": primary.get("bevoegdGezag"),
        "bestuurslaag": primary.get("bestuurslaag"),
        "regeling": primary.get("regeling"),
        "procedureType": primary.get("procedureType"),
        "manualReviewRequired": manual,
        "manualReviewReason": "; ".join(reasons),
        "appliedRules": list(dict.fromkeys(applied)),
        "sourceRefs": list({ref.get("url", "") + ref.get("section", ""): ref for ref in source_refs}.values()),
    }
