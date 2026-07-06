from dataclasses import dataclass


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


@dataclass
class DienstverleningRequest:
    organisatie: str
    productNaam: str
    bestuurslaag: str


def _find_product(products: list[dict], name: str) -> dict | None:
    needle = _norm(name)
    for product in products:
        names = {_norm(product.get("name", "")), _norm(product.get("id", ""))}
        if needle in names:
            return product
    return None


def _find_organisation(organisations: list[dict], value: str) -> dict | None:
    needle = _norm(value)
    for org in organisations:
        names = {
            _norm(org.get("code", "")),
            _norm(org.get("name", "")),
            _norm(org.get("officialName", "")),
        }
        if needle in names:
            return org
    return None


def check_dienstverlening(req: DienstverleningRequest, products: list[dict], organisations: list[dict]) -> dict:
    product = _find_product(products, req.productNaam)
    org = _find_organisation(organisations, req.organisatie)
    requested_layer = _norm(req.bestuurslaag)

    applied = []
    source_refs = []
    manual = False
    reasons = []

    if product:
        applied.append("DVC-001")
        source_refs.extend(product.get("sourceRefs", []))
    else:
        applied.append("DVC-010")
        manual = True
        reasons.append("Productnaam niet gevonden in UPL.")

    if org:
        applied.append("DVC-006")
        source_refs.extend(org.get("sourceRefs", []))
        if requested_layer and org.get("bestuurslaag") != requested_layer:
            manual = True
            reasons.append("Organisatie hoort niet bij opgegeven bestuurslaag.")
    else:
        applied.append("DVC-010")
        manual = True
        reasons.append("Organisatie niet gevonden in TOOI/ROO.")

    layer_fit = False
    if product and requested_layer in product.get("bestuurslagen", []):
        layer_fit = True
        applied.append({
            "gemeente": "DVC-002",
            "provincie": "DVC-003",
            "waterschap": "DVC-004",
            "rijk": "DVC-005",
        }.get(requested_layer, "DVC-001"))
    elif product:
        applied.append("DVC-009")
        manual = True
        reasons.append("UPL product hoort niet bij opgegeven bestuurslaag.")

    signals = product.get("signals", {}) if product else {}
    if signals.get("sdg"):
        applied.append("DVC-007")
    if requested_layer == "gemeente" and signals.get("wmebv"):
        applied.append("DVC-008")

    return {
        "uniformeProductnaam": product.get("name") if product else None,
        "organisatie": org.get("officialName") if org else None,
        "bestuurslaag": requested_layer,
        "bestuurslaagfit": layer_fit,
        "signals": {
            "sdg": bool(signals.get("sdg")),
            "wmebv": bool(signals.get("wmebv")),
            "aanvraag": bool(signals.get("aanvraag")),
            "melding": bool(signals.get("melding")),
            "verplichting": bool(signals.get("verplichting")),
            "subsidie": bool(signals.get("subsidie")),
        },
        "manualReviewRequired": manual,
        "manualReviewReason": "; ".join(reasons),
        "appliedRules": list(dict.fromkeys(applied)),
        "sourceRefs": source_refs,
    }
