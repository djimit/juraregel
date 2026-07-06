#!/usr/bin/env python3
"""Gate 14: Jurist-acceptatie check. SKIP voor drafts (geen juristAccordering)."""
import json, sys
from datetime import datetime
from pathlib import Path


def _parse_iso_date(value: str, field: str) -> tuple[datetime | None, str | None]:
    if not value:
        return None, f"juristAccordering.{field} ontbreekt"
    try:
        return datetime.fromisoformat(value), None
    except Exception:
        return None, f"Ongeldige {field} datum: {value}"

def check_acceptatie(jrem_path: str) -> tuple[str, str]:
    """Returns (status, message). status: PASS, FAIL, or SKIP."""
    with open(jrem_path) as f:
        data = json.load(f)
    
    metadata = data.get("metadata", {})
    acceptatie_type = metadata.get("acceptatieType", "draft")
    accordering = metadata.get("juristAccordering")
    
    # SKIP for drafts (no juristAccordering)
    if not accordering or acceptatie_type == "draft":
        return "SKIP", f"Draft JREM (acceptatieType={acceptatie_type}) — geen jurist-acceptatie vereist"
    
    naam = accordering.get("geaccondeerdDoor", "")
    if not naam:
        return "FAIL", "juristAccordering.geaccondeerdDoor is leeg"

    datum, err = _parse_iso_date(accordering.get("datum"), "datum")
    if err:
        return "FAIL", err

    geldig_tot = accordering.get("geldigTot")
    gt, err = _parse_iso_date(geldig_tot, "geldigTot")
    if err:
        return "FAIL", err
    if gt.date() < datetime.now().date():
        return "FAIL", f"Acceptatie verlopen op {geldig_tot}"

    accorderings_versie = accordering.get("versie", "")
    jrem_versie = data.get("version", "")
    if not accorderings_versie:
        return "FAIL", "juristAccordering.versie ontbreekt"
    if accorderings_versie != jrem_versie:
        return "FAIL", f"Acceptatie versie ({accorderings_versie}) komt niet overeen met JREM versie ({jrem_versie})"
    
    return "PASS", f"Acceptatie geldig: {naam}, tot {geldig_tot}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: acceptatie-check.py <jrem-file>")
        sys.exit(2)
    status, msg = check_acceptatie(sys.argv[1])
    print(f"Gate 14/14: Jurist-acceptatie — {status}: {msg}")
    sys.exit(0 if status != "FAIL" else 1)
