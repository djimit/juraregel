import hashlib
from datetime import datetime, timezone
"""Publicatie Rule API — UC-06."""
import sys
from pathlib import Path
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("publicatie", JREM_DIR, 8493)
if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8493)


# ─── C1: PII Check Endpoint met V4.2 Engine ───
from pydantic import BaseModel as PydanticModel
from typing import Optional

class PiiCheckRequest(PydanticModel):
    bodyText: str
    ecli: Optional[str] = None
    rechtsgebied: Optional[str] = None

class PiiClassificatie(PydanticModel):
    gegevenType: str
    match: str
    startIdx: int
    persoonType: str
    status: str
    reden: str
    sentence: str = ""

@app.post("/v1/publicatie/check-pii")
def check_pii(request: PiiCheckRequest):
    """Check body_text for PII using V4.2 pseudonimiseringsrichtlijn engine."""
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.insert(0, str(_Path(__file__).parent.parent / "lib"))
    
    try:
        from richtlijn_engine_v4 import scan_met_richtlijn_v4, detect_rechtsgebied, PersoonType, PseudonimiseringsStatus
    except ImportError:
        raise HTTPException(status_code=503, detail="V4.2 engine not available")
    
    # Detect rechtsgebied from ECLI
    rg = request.rechtsgebied or (detect_rechtsgebied(request.ecli) if request.ecli else "civiel")
    
    # Run V4.2 engine
    result = scan_met_richtlijn_v4(request.bodyText, request.ecli or "", rg)
    
    # Build classificaties
    classificaties = []
    geanonimiseerde_tekst = list(request.bodyText)
    token_map = {
        "date_of_birth": "[geboortedatum]",
        "street_address": "[adres]",
        "postcode": "[postcode]",
        "email": "[e-mailadres]",
        "phone_mobile": "[telefoonnummer]",
        "phone_landline": "[telefoonnummer]",
        "bsn": "[BSN]",
        "license_plate": "[kenteken]",
    }
    
    from richtlijn_engine_v4 import get_sentence
    
    for d in result.decisions:
        cls = {
            "gegevenType": d.gegeven_type,
            "match": d.match,
            "startIdx": d.start_idx,
            "persoonType": d.persoon_type.value,
            "status": d.status.value,
            "reden": d.reden,
            "sentence": get_sentence(request.bodyText, d.start_idx)[:200],
        }
        classificaties.append(cls)
        
        # Token replacement for pseudonimiseer
        if d.status == PseudonimiseringsStatus.PSEUDONIMISEER:
            token = token_map.get(d.gegeven_type, f"[{d.gegeven_type}]")
            for i in range(d.start_idx, min(d.end_idx, len(geanonimiseerde_tekst))):
                if i == d.start_idx:
                    geanonimiseerde_tekst[i] = token
                else:
                    geanonimiseerde_tekst[i] = ""
    
    geanonimiseerd = "".join(geanonimiseerde_tekst)
    
    # Source refs from JREM
    from api_base import load_jrem
    jrem_dir = Path(__file__).parent.parent / "jrem" / "exports"
    try:
        jrem = load_jrem(jrem_dir, "2025.1")
        source_refs = jrem.get("metadata", {}).get("juridischeContext", {})
    except:
        source_refs = {}
    
    return {
        "classificaties": classificaties,
        "tePseudonimiseren": result.te_pseudonimiseren,
        "nietPseudonimiseren": result.niet_pseudonimiseren,
        "manualReview": result.handmatige_controle,
        "geanonimiseerdeTekst": geanonimiseerd,
        "rapport": {
            "totaal": result.totaal_gedetecteerd,
            "bronverwijzing": "Pseudonimiseringsrichtlijn Rechtspraak.nl",
            "juridischeContext": source_refs,
        },
        "audit": {
            "inputHash": f"sha256:{__import__("hashlib").sha256(request.bodyText.encode()).hexdigest()}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    }
