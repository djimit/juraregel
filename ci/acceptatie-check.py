#!/usr/bin/env python3
"""Gate 14: Jurist-acceptatie check. SKIP voor drafts (geen juristAccordering)."""
import json, sys
from datetime import datetime
from pathlib import Path

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
    
    # Check geaccondeerdDoor
    naam = accordering.get("geaccondeerdDoor", "")
    if not naam:
        return "FAIL", "juristAccordering.geaccondeerdDoor is leeg"
    
    # Check geldigTot not expired
    geldig_tot = accordering.get("geldigTot")
    if geldig_tot:
        try:
            gt = datetime.fromisoformat(geldig_tot)
            if gt < datetime.now():
                return "FAIL", f"Acceptatie verlopen op {geldig_tot}"
        except Exception:
            return "FAIL", f"Ongeldige geldigTot datum: {geldig_tot}"
    
    # Check versie matches JREM version
    accorderings_versie = accordering.get("versie", "")
    jrem_versie = data.get("version", "")
    if accorderings_versie and accorderings_versie != jrem_versie:
        return "FAIL", f"Acceptatie versie ({accorderings_versie}) komt niet overeen met JREM versie ({jrem_versie})"
    
    return "PASS", f"Acceptatie geldig: {naam}, tot {geldig_tot}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: acceptatie-check.py <jrem-file>")
        sys.exit(2)
    status, msg = check_acceptatie(sys.argv[1])
    print(f"Gate 14/14: Jurist-acceptatie — {status}: {msg}")
    sys.exit(0 if status != "FAIL" else 1)
