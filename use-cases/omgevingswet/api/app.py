from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException
import json, hashlib
from datetime import datetime, timezone

from api_base import create_app, load_jrem, select_rule

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("omgevingswet", JREM_DIR, 8515, calculate_capability=True)

# Remove factory's calculate endpoint (expects CalculateRequest, not domain-specific input)
app.router.routes = [r for r in app.router.routes if not (hasattr(r, 'path') and r.path == f'/v1/omgevingswet/calculate' and hasattr(r, 'methods') and 'POST' in r.methods)]

_jrem = load_jrem(JREM_DIR, "2025.1")

class OmgevingswetRequest(BaseModel):
    activiteit: Optional[str] = None
    bouwhoogte: Optional[float] = None
    volume: Optional[float] = None
    boomHoogte: Optional[float] = None
    stamomtrek: Optional[float] = None
    geluidsniveau: Optional[float] = None
    locatie: Optional[str] = None
    locatieType: Optional[str] = None
    monument: Optional[bool] = None
    tijdelijk: Optional[bool] = None
    beschermdeSoort: Optional[bool] = None

@app.post("/v1/omgevingswet/calculate")
def calculate_omgevingswet(request: OmgevingswetRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
            outcome = rule["outcome"]
            input_hash = hashlib.sha256(request.model_dump_json().encode()).hexdigest()[:16]
            return {
                "calculationId": f"calc-{input_hash}",
                "ruleSetVersion": _jrem["version"],
                "domain": "omgevingswet",
                "result": {"matchedRule": {"ruleId": rule["ruleId"], "name": rule["name"]}, "outcome": outcome},
                "explanation": {"summary": rule["name"], "appliedRules": [rule["ruleId"]], "sourceRefs": rule.get("sourceRefs", [])},
                "audit": {"inputHash": f"sha256:{input_hash}", "rulesetHash": f"sha256:{hashlib.sha256(json.dumps(_jrem, sort_keys=True).encode()).hexdigest()[:16]}", "timestamp": datetime.now(timezone.utc).isoformat()}
            }
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")

@app.post("/v1/omgevingswet/explain")
def explain_omgevingswet(request: OmgevingswetRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
        return {"summary": rule["name"], "appliedRules": [rule["ruleId"]], "sourceRefs": rule.get("sourceRefs", []), "conditions": rule.get("conditions", {}), "outcome": rule["outcome"]}
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")
