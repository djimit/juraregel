from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Any
from fastapi import HTTPException
import json, hashlib
from datetime import datetime, timezone

from api_base import create_app, load_jrem, select_rule

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("participatiewet", JREM_DIR, 8517, calculate_capability=True)

# Remove factory's calculate endpoint (expects CalculateRequest, not domain-specific input)
app.router.routes = [r for r in app.router.routes if not (hasattr(r, 'path') and r.path == f'/v1/participatiewet/calculate' and hasattr(r, 'methods') and 'POST' in r.methods)]

_jrem = load_jrem(JREM_DIR, "2025.1")

class ParticipatiewetRequest(BaseModel):
    huishoudenType: Optional[str] = None
    leeftijd: Optional[int] = None
    alleenstaande: Optional[bool] = None
    medebewoners: Optional[int] = None
    medebewonerZelfstandigeHuishouding: Optional[bool] = None
    vermogen: Optional[float] = None
    inkomen: Optional[Any] = None
    inkomenUitWerk: Optional[bool] = None
    maandenAanHetWerk: Optional[int] = None
    verwijtbareWerkloosheid: Optional[bool] = None
    uitkeringOntvangen: Optional[bool] = None
    arbeidsgeschikt: Optional[bool] = None
    arbeidsbeperking: Optional[bool] = None
    doelgroepregister: Optional[bool] = None
    alleenstaandMetLangeDuur: Optional[bool] = None

@app.post("/v1/participatiewet/calculate")
def calculate_participatiewet(request: ParticipatiewetRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
            outcome = rule["outcome"]
            input_hash = hashlib.sha256(request.model_dump_json().encode()).hexdigest()[:16]
            return {
                "calculationId": f"calc-{input_hash}",
                "ruleSetVersion": _jrem["version"],
                "domain": "participatiewet",
                "result": {"matchedRule": {"ruleId": rule["ruleId"], "name": rule["name"]}, "outcome": outcome},
                "explanation": {"summary": rule["name"], "appliedRules": [rule["ruleId"]], "sourceRefs": rule.get("sourceRefs", [])},
                "audit": {"inputHash": f"sha256:{input_hash}", "rulesetHash": f"sha256:{hashlib.sha256(json.dumps(_jrem, sort_keys=True).encode()).hexdigest()[:16]}", "timestamp": datetime.now(timezone.utc).isoformat()}
            }
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")

@app.post("/v1/participatiewet/explain")
def explain_participatiewet(request: ParticipatiewetRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
        return {"summary": rule["name"], "appliedRules": [rule["ruleId"]], "sourceRefs": rule.get("sourceRefs", []), "conditions": rule.get("conditions", {}), "outcome": rule["outcome"]}
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")
