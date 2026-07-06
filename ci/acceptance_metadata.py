from __future__ import annotations

from datetime import date


BASE_FIELDS = ("geaccondeerdDoor", "datum", "geldigTot", "versie")
EXTENDED_FIELDS = ("rol", "organisatie", "scope", "bronSnapshot", "verklaring", "beperkingen")


def _is_strict_maturity(maturity: str) -> bool:
    return (maturity or "").startswith(("L2-", "L3-"))


def _parse_date(value: str, field: str) -> tuple[date | None, str | None]:
    if not value:
        return None, f"juristAccordering.{field} ontbreekt"
    try:
        return date.fromisoformat(value), None
    except ValueError:
        return None, f"Ongeldige {field} datum: {value}"


def validate_acceptance(
    data: dict,
    require_extended: bool = False,
    today: date | None = None,
) -> tuple[str, str]:
    """Return PASS, FAIL or SKIP for JREM jurist acceptance metadata."""
    metadata = data.get("metadata", {})
    acceptatie_type = metadata.get("acceptatieType", "draft")
    accordering = metadata.get("juristAccordering")
    strict = require_extended or _is_strict_maturity(data.get("maturityLevel", ""))

    if not accordering or acceptatie_type == "draft":
        if strict:
            return "FAIL", "L2/L3 vereist volledige juristAccordering"
        return "SKIP", f"Draft JREM (acceptatieType={acceptatie_type}) - geen jurist-acceptatie vereist"

    for field in BASE_FIELDS:
        if not accordering.get(field):
            return "FAIL", f"juristAccordering.{field} ontbreekt"

    geldig_tot, err = _parse_date(accordering.get("geldigTot"), "geldigTot")
    if err:
        return "FAIL", err
    if geldig_tot < (today or date.today()):
        return "FAIL", f"Acceptatie verlopen op {accordering.get('geldigTot')}"

    _, err = _parse_date(accordering.get("datum"), "datum")
    if err:
        return "FAIL", err

    if accordering.get("versie") != data.get("version", ""):
        return (
            "FAIL",
            f"Acceptatie versie ({accordering.get('versie')}) komt niet overeen met JREM versie ({data.get('version', '')})",
        )

    if strict:
        for field in EXTENDED_FIELDS:
            value = accordering.get(field)
            if field == "beperkingen":
                if not isinstance(value, list) or not value:
                    return "FAIL", "juristAccordering.beperkingen ontbreekt"
            elif not value:
                return "FAIL", f"juristAccordering.{field} ontbreekt"

    return "PASS", f"Acceptatie geldig: {accordering.get('geaccondeerdDoor')}, tot {accordering.get('geldigTot')}"


def validate_l3_boundary(data: dict) -> tuple[str, str]:
    maturity = data.get("maturityLevel", "")
    if not maturity.startswith("L3-"):
        return "PASS", "Niet L3"

    metadata = data.get("metadata", {})
    if not metadata.get("indicatorDisclaimer"):
        return "FAIL", "L3 indicatorDisclaimer ontbreekt"
    if metadata.get("manualReviewBoundary") != "indicator-only":
        return "FAIL", "L3 manualReviewBoundary moet indicator-only zijn"
    return "PASS", "L3 indicatorgrens aanwezig"
