from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional, Any
from fastapi import HTTPException
import json
import hashlib
from datetime import datetime, timezone

from api_base import create_app, load_jrem

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("toeslagen", JREM_DIR, 8514)

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

def _matches(val: Any, cond: Any) -> bool:
    if cond is None: return True
    if val is None: return False
    if isinstance(cond, str): return val == cond
    if isinstance(cond, list): return val in cond
    if isinstance(cond, dict):
        if "periode" in cond: cond = {k:v for k,v in cond.items() if k != "periode"}
        if not isinstance(val, (int, float)): return False
        if "gt" in cond and not (val > cond["gt"]): return False
        if "gte" in cond and not (val >= cond["gte"]): return False
        if "lt" in cond and not (val < cond["lt"]): return False
        if "lte" in cond and not (val <= cond["lte"]): return False
        return True
    return val == cond

def _match_rule(rule: dict, req: ToeslagRequest) -> bool:
    cond = rule.get("conditions", {})
    data = req.model_dump()
    for key, condition in cond.items():
        if key == "periode": continue  # metadata, not a condition
        val = data.get(key)
        if isinstance(condition, dict) and isinstance(val, dict):
            # e.g. huur: {"lte": 879.12, "periode": "maandelijks"}
            if "periode" in condition: condition = {k:v for k,v in condition.items() if k != "periode"}
            if not isinstance(val, (int, float)):
                # huur might be just a number
                if "huur" in key: val = data.get("huur")
        if not _matches(val, condition):
            return False
    return True

@app.post("/v1/toeslagen/calculate")
def calculate_toeslag(request: ToeslagRequest):
    sorted_rules = sorted(_jrem["rules"], key=lambda r: r.get("priority", 0), reverse=True)
    for rule in sorted_rules:
        if _match_rule(rule, request):
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
    sorted_rules = sorted(_jrem["rules"], key=lambda r: r.get("priority", 0), reverse=True)
    for rule in sorted_rules:
        if _match_rule(rule, request):
            return {
                "summary": rule["name"],
                "appliedRules": [rule["ruleId"]],
                "sourceRefs": rule.get("sourceRefs", []),
                "conditions": rule.get("conditions", {}),
                "outcome": rule["outcome"]
            }
    raise HTTPException(status_code=404, detail="Geen passende regel gevonden")
