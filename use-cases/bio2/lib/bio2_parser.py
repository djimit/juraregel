"""
BIO2 Maatregelen Parser — parse MinBZK GitHub Markdown naar gestructureerde maatregelen.

Haalt de BIO2 maatregelen op via GitHub API en extraheert:
- maatregelId (### N.NN.NN headers)
- categorie (## Categorie N: [naam])
- beschrijving (tekst na header)
- isoRef (eerste 3 cijfers van maatregelId → ISO 27002 clause)
- isOverheidsMaatregel (boolean — "Geen overheidsmaatregel" = False)
- alias (doel-maatregelId bij "Verplaatst naar N.NN.NN")
"""

import re
import base64
import json
import subprocess
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Maatregel:
    maatregelId: str
    categorie: str
    categorieNummer: str
    beschrijving: str
    isoRef: str
    isOverheidsMaatregel: bool
    alias: Optional[str] = None

CATEGORIE_MAP = {
    "5": "organisatorisch",
    "6": "mensgericht",
    "7": "fysiek",
    "8": "technologisch",
}

def fetch_bio2_markdown() -> str:
    """Haal BIO2 maatregelen Markdown van MinBZK GitHub via gh api."""
    result = subprocess.run(
        ["gh", "api", "repos/MinBZK/Baseline-Informatiebeveiliging-Overheid/contents/docs/maatregelen/index.md",
         "--jq", ".content"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"GitHub API failed: {result.stderr}")
    return base64.b64decode(result.stdout.strip()).decode("utf-8")

def parse_maatregelen(markdown: str = None) -> list[Maatregel]:
    """
    Parse BIO2 Markdown naar gestructureerde maatregelen.
    Als markdown=None, haal van GitHub.
    """
    if markdown is None:
        markdown = fetch_bio2_markdown()
    
    maatregelen = []
    current_categorie = ""
    current_categorie_num = ""
    
    lines = markdown.split("\n")
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Detect categorie header: ## Categorie 5: Organisatorische maatregelen
        cat_match = re.match(r"^##\s+Categorie\s+(\d+):\s+(.+)", line)
        if cat_match:
            current_categorie_num = cat_match.group(1)
            current_categorie = cat_match.group(2).strip()
            i += 1
            continue
        
        # Detect maatregel header: ### 5.01.01
        maatregel_match = re.match(r"^###\s+(\d+\.\d+\.\d+)", line)
        if maatregel_match:
            maatregel_id = maatregel_match.group(1)
            
            # Collect description (lines until next ### or ## or end)
            desc_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("###") and not lines[i].startswith("## "):
                desc_lines.append(lines[i])
                i += 1
            
            beschrijving = "\n".join(desc_lines).strip()
            
            # Determine ISO ref (first 3 digits → ISO 27002 clause)
            parts = maatregel_id.split(".")
            iso_ref = f"ISO 27002 {parts[0]}.{parts[1]}"
            
            # Check if "Geen overheidsmaatregel"
            is_overheids = True
            alias = None
            
            if "Geen overheidsmaatregel" in beschrijving:
                is_overheeds = False
            
            # Check if "Verplaatst naar"
            verplaatst_match = re.search(r"Verplaatst naar\s+(\d+\.\d+\.\d+)", beschrijving)
            if verplaatst_match:
                alias = verplaatst_match.group(1)
                is_overheids = False
            
            maatregelen.append(Maatregel(
                maatregelId=maatregel_id,
                categorie=current_categorie,
                categorieNummer=current_categorie_num,
                beschrijving=beschrijving[:500],  # truncate for storage
                isoRef=iso_ref,
                isOverheidsMaatregel=is_overheids,
                alias=alias,
            ))
            continue
        
        i += 1
    
    return maatregelen

def maatregelen_to_jrem(maatregelen: list[Maatregel], bio_versie: str = "1.2") -> dict:
    """Converteer maatregelen naar JREM export format."""
    rules = []
    scenarios = []
    
    for m in maatregelen:
        if not m.isOverheidsMaatregel:
            continue  # Skip "Geen overheidsmaatregel" — ISO-only
        
        rule_id = f"BIO2-{m.maatregelId}"
        
        # Create JREM rule
        rules.append({
            "ruleId": rule_id,
            "name": m.beschrijving[:100].replace("\n", " ").strip() or f"Maatregel {m.maatregelId}",
            "priority": 100,
            "legalStatus": "wettelijk",
            "sourceRefs": [
                {
                    "type": "wetsartikel",
                    "title": "BIO2 — Baseline Informatiebeveiliging Overheid",
                    "section": f"Maatregel {m.maatregelId}",
                    "url": "https://www.bio-overheid.nl/category/producten/bio"
                },
                {
                    "type": "wetsartikel",
                    "title": "NEN-EN-ISO/IEC 27002",
                    "section": m.isoRef,
                    "url": "https://www.iso.org/standard/27001"
                }
            ],
            "conditions": {},
            "outcome": {
                "griffierecht": {"amount": None, "currency": "EUR"},
                "category": f"bio2_{m.categorie}",
                "confidence": "deterministic",
                "manualReviewRequired": False
            },
            "examples": [
                {"input": {"maatregelId": m.maatregelId, "implementatie": "ja"}, "expectedAmount": 0}
            ]
        })
        
        # Create scenario per maatregel
        scenarios.append({
            "id": f"BIO2-SC-{m.maatregelId}",
            "description": f"Maatregel {m.maatregelId} — {m.categorie}",
            "input": {
                "rechtsgebied": "bio2",
                "zaakstroom": "handel",
                "procedureType": "dagvaarding",
                "vorderingWaarde": 0,
                "bijzondereCategorie": m.maatregelId,
            },
            "expected": {
                "griffierecht": 0,
                "category": f"bio2_{m.categorie}",
                "appliedRules": [rule_id]
            }
        })
    
    from datetime import datetime, timedelta
    now = datetime.now()
    geldig_tot = (now + timedelta(days=365)).date().isoformat()
    
    return {
        "schemaVersion": "1.0.0",
        "ruleSetId": "bio2-maatregelen",
        "version": bio_versie,
        "validFrom": "2025-01-01",
        "validUntil": "2026-12-31",
        "jurisdiction": "NL",
        "domain": "bio2-informatiebeveiliging",
        "procedureType": "dagvaarding",
        "conflictResolution": "first-match",
        "rules": rules,
        "scenarios": scenarios[:20],  # First 20 scenarios for JREM
        "transitionRules": [],
        "metadata": {
            "juridischeContext": {
                "wet": "BIO2",
                "wetBwbrId": "BWBR0044701",
                "wetVersieLaatstGecheckt": now.date().isoformat(),
                "tariefVersie": bio_versie
            },
            "bronverificatieDatum": now.date().isoformat(),
            "acceptatieType": "draft"
        }
    }

if __name__ == "__main__":
    maatregelen = parse_maatregelen()
    print(f"Geparseerd: {len(maatregelen)} maatregelen")
    for m in maatregelen[:5]:
        print(f"  {m.maatregelId} [{m.categorie}] ISO={m.isoRef} overheids={m.isOverheidsMaatregel} alias={m.alias}")
    print(f"  ...")
    
    overheads = [m for m in maatregelen if m.isOverheidsMaatregel]
    niet_overheads = [m for m in maatregelen if not m.isOverheidsMaatregel]
    print(f"  Overheidsmaatregelen: {len(overheads)}")
    print(f"  Geen overheidsmaatregel (ISO-only): {len(niet_overheads)}")
    
    # Per categorie
    from collections import Counter
    cat_count = Counter(m.categorie for m in maatregelen)
    for cat, cnt in cat_count.most_common():
        print(f"  Categorie '{cat}': {cnt}")
