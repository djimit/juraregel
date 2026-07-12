from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
from fastapi import HTTPException
import json
import hashlib
from datetime import datetime, timezone

from api_base import create_app, load_jrem, select_rule

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("toeslagen", JREM_DIR, 8514, calculate_capability=True)

# Remove factory's calculate endpoint (expects CalculateRequest, not domain-specific input)
app.router.routes = [r for r in app.router.routes if not (hasattr(r, 'path') and r.path == f'/v1/toeslagen/calculate' and hasattr(r, 'methods') and 'POST' in r.methods)]

_jrem = load_jrem(JREM_DIR, "2025.1")

class ToeslagRequest(BaseModel):
    toeslagType: str = Field(..., description="zorgtoeslag, huurtoeslag, kinderopvangtoeslag, kindgebonden_budget")
    leeftijd: Optional[int] = None
    alleenstaande: Optional[bool] = None
    toeslagenpartner: Optional[bool] = None
    inkomen: Optional[float] = None
    huur: Optional[float] = None
    kindOpOpvang: Optional[bool] = None
    heeftKind: Optional[bool] = None
    nationaliteit: Optional[str] = None
    verblijfsrecht: Optional[bool] = None
    gedetineerd: Optional[bool] = None
    woonsituatie: Optional[str] = None

@app.post("/v1/toeslagen/calculate")
def calculate_toeslag(request: ToeslagRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
            outcome = rule["outcome"]
            input_hash = hashlib.sha256(request.model_dump_json().encode()).hexdigest()[:16]
            return {
                "calculationId": f"calc-{input_hash}",
                "ruleSetVersion": _jrem["version"],
                "domain": "toeslagen",
                "result": {
                    "matchedRule": {"ruleId": rule["ruleId"], "name": rule["name"]},
                    "outcome": outcome
                },
                "explanation": {
                    "summary": rule["name"],
                    "appliedRules": [rule["ruleId"]],
                    "sourceRefs": rule.get("sourceRefs", [])
                },
                "audit": {
                    "inputHash": f"sha256:{input_hash}",
                    "rulesetHash": f"sha256:{hashlib.sha256(json.dumps(_jrem, sort_keys=True).encode()).hexdigest()[:16]}",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden voor deze input")

@app.post("/v1/toeslagen/explain")
def explain_toeslag(request: ToeslagRequest):
    rule = select_rule(_jrem["rules"], request.model_dump())
    if rule:
            return {
                "summary": rule["name"],
                "appliedRules": [rule["ruleId"]],
                "sourceRefs": rule.get("sourceRefs", []),
                "conditions": rule.get("conditions", {}),
                "outcome": rule["outcome"]
            }
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")
