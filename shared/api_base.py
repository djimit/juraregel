"""
Legal RuleOps Platform — Shared API Base.

Factory pattern: create_app(domain, jrem_dir, port) → FastAPI instance.
Elke use case roept create_app aan met eigen domein, JREM path, en poort.

Bevat: JREM loading, rule matching, hash computation, audit store,
input validatie, juridischeContext, error handling, structured output.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# ─── Models ───

class ZaakInput(BaseModel):
    rechtsgebied: str = "civiel"
    zaakstroom: str = Field(..., description="kanton of handel")
    procedureType: str = Field(..., description="dagvaarding")
    vorderingWaarde: float | str | None = Field(None, description="Bedrag of 'onbepaald'")
    bijzondereCategorie: str = "geen"

    @field_validator("zaakstroom")
    @classmethod
    def validate_zaakstroom(cls, v):
        if v not in ("kanton", "handel"):
            raise ValueError("zaakstroom moet 'kanton' of 'handel' zijn")
        return v

    @field_validator("vorderingWaarde")
    @classmethod
    def validate_vordering(cls, v):
        if v == "onbepaald":
            return v
        if v is not None and isinstance(v, (int, float)) and v < 0:
            raise ValueError("vorderingWaarde mag niet negatief zijn")
        return v


class PartijInput(BaseModel):
    rol: str = Field(..., description="eiser, gedaagde, verzoeker, verweerder")
    partijType: str = Field(..., description="natuurlijk_persoon, niet_natuurlijk_persoon, onvermogend")
    onvermogend: bool = False
    verweerStatus: str = "n.v.t."

    @field_validator("rol")
    @classmethod
    def validate_rol(cls, v):
        if v not in ("eiser", "gedaagde", "verzoeker", "verweerder"):
            raise ValueError("rol moet eiser, gedaagde, verzoeker of verweerder zijn")
        return v

    @field_validator("partijType")
    @classmethod
    def validate_partij_type(cls, v):
        if v not in ("natuurlijk_persoon", "niet_natuurlijk_persoon", "onvermogend"):
            raise ValueError("partijType moet natuurlijk_persoon, niet_natuurlijk_persoon of onvermogend zijn")
        return v

    @field_validator("verweerStatus")
    @classmethod
    def validate_verweer_status(cls, v):
        if v not in ("niet_ingediend", "ingediend", "onbekend", "n.v.t."):
            raise ValueError("verweerStatus moet niet_ingediend, ingediend, onbekend of n.v.t. zijn")
        return v


class CalculateRequest(BaseModel):
    calculationDate: str = Field(..., description="ISO 8601 datum")
    zaak: ZaakInput
    partij: PartijInput
    zaakIdentificatie: Optional[str] = None
    tariefjaar: Optional[int] = None


# ─── JREM Loading ───

_jrem_cache: dict[str, dict] = {}

def load_jrem(jrem_dir: Path, version: str = "2026.1") -> dict:
    """Load a JREM export by version string."""
    cache_key = f"{jrem_dir}:{version}"
    if cache_key in _jrem_cache:
        return _jrem_cache[cache_key]
    pattern = f"*-{version}.json"
    files = list(jrem_dir.glob(pattern))
    if not files:
        year = version.split(".")[0]
        files = list(jrem_dir.glob(f"*-{year}.*.json"))
    if not files:
        raise FileNotFoundError(f"No JREM export found in {jrem_dir} for version {version}")
    with open(files[0]) as f:
        data = json.load(f)
    _jrem_cache[cache_key] = data
    return data


def list_versions(jrem_dir: Path) -> list[dict]:
    """List all available JREM export versions in a directory."""
    versions = []
    for filepath in sorted(jrem_dir.glob("*.json")):
        with open(filepath) as f:
            data = json.load(f)
        versions.append({
            "version": data["version"],
            "validFrom": data["validFrom"],
            "validUntil": data["validUntil"],
            "ruleCount": len(data["rules"]),
            "scenarioCount": len(data.get("scenarios", [])),
            "hasAcceptatie": bool(data.get("metadata", {}).get("juristAccordering", {}).get("geaccondeerdDoor")),
        })
    return versions


def select_version(jrem_dir: Path, calculation_date: str, tariefjaar: Optional[int] = None) -> str:
    """Select the applicable JREM version based on calculation date."""
    if tariefjaar:
        year = str(tariefjaar)
    else:
        try:
            dt = datetime.fromisoformat(calculation_date.replace("Z", "+00:00"))
            year = str(dt.year)
        except Exception:
            year = "2026"
    for v in list_versions(jrem_dir):
        if v["version"].startswith(year):
            return v["version"]
    all_v = list_versions(jrem_dir)
    return all_v[-1]["version"] if all_v else "2026.1"


# ─── Rule Matching ───

def matches_condition(value, condition) -> bool:
    if condition is None:
        return True
    if isinstance(condition, str):
        return value == condition
    if isinstance(condition, list):
        return value in condition
    if isinstance(condition, dict):
        if isinstance(value, str) and value == "onbepaald":
            return False
        if value is None or not isinstance(value, (int, float)):
            return False
        result = True
        if "gt" in condition: result = result and value > condition["gt"]
        if "gte" in condition: result = result and value >= condition["gte"]
        if "lt" in condition: result = result and value < condition["lt"]
        if "lte" in condition: result = result and value <= condition["lte"]
        return result
    return False


def match_rule(rule: dict, request: CalculateRequest) -> bool:
    conditions = rule.get("conditions", {})
    if "zaakstroom" in conditions and not matches_condition(request.zaak.zaakstroom, conditions["zaakstroom"]): return False
    if "rol" in conditions and not matches_condition(request.partij.rol, conditions["rol"]): return False
    if "partijType" in conditions:
        effective = "onvermogend" if request.partij.onvermogend else request.partij.partijType
        if not matches_condition(effective, conditions["partijType"]): return False
    if "verweerStatus" in conditions and not matches_condition(request.partij.verweerStatus, conditions["verweerStatus"]): return False
    if "bijzondereCategorie" in conditions and not matches_condition(request.zaak.bijzondereCategorie, conditions["bijzondereCategorie"]): return False
    if "vorderingWaarde" in conditions:
        vw = request.zaak.vorderingWaarde
        if isinstance(conditions["vorderingWaarde"], str) and conditions["vorderingWaarde"] == "onbepaald":
            if vw != "onbepaald": return False
        elif isinstance(conditions["vorderingWaarde"], dict):
            if vw == "onbepaald" or vw is None: return False
            if not matches_condition(vw, conditions["vorderingWaarde"]): return False
    return True


def build_reasoning_steps(rule: dict, request: CalculateRequest) -> list[str]:
    steps = []
    if request.zaak.rechtsgebied == "civiel":
        steps.append(f"Rechtsgebied is civiel → griffierecht is verschuldigd")
    else:
        steps.append(f"Rechtsgebied is {request.zaak.rechtsgebied} → niet in scope")
        return steps
    steps.append(f"Zaakstroom is {request.zaak.zaakstroom}")
    steps.append(f"Proceduretype is {request.zaak.procedureType}")
    if request.partij.rol == "gedaagde":
        if request.partij.verweerStatus == "ingediend":
            steps.append("Partij is gedaagde en verweer is ingediend → griffierecht verschuldigd")
        elif request.partij.verweerStatus == "niet_ingediend":
            steps.append("Partij is gedaagde en geen verweer → geen griffierecht")
        elif request.partij.verweerStatus == "onbekend":
            steps.append("Partij is gedaagde, verweerStatus onbekend → handmatige controle")
    else:
        steps.append(f"Partij is {request.partij.rol} → griffierecht verschuldigd door {request.partij.rol}")
    effective_type = "onvermogend" if request.partij.onvermogend else request.partij.partijType
    steps.append(f"Partijtype is {effective_type}")
    vw = request.zaak.vorderingWaarde
    steps.append("Vorderingwaarde is onbepaald" if vw in ("onbepaald", None) else f"Vorderingwaarde is €{vw:,.2f}")
    outcome = rule.get("outcome", {})
    steps.append(f"Tariefcategorie: {outcome.get('category', 'onbekend')}")
    amount = outcome.get("griffierecht", {}).get("amount")
    steps.append(f"Griffierecht: €{amount}" if amount is not None else "Geen griffierecht verschuldigd")
    return steps


def build_summary(rule: dict, request: CalculateRequest) -> str:
    outcome = rule.get("outcome", {})
    amount = outcome.get("griffierecht", {}).get("amount")
    category = outcome.get("category", "onbekend")
    effective_type = "onvermogend" if request.partij.onvermogend else request.partij.partijType
    vw = request.zaak.vorderingWaarde
    vw_desc = "een onbepaalde waarde" if vw in ("onbepaald", None) else f"een vordering van €{vw:,.2f}"
    if amount is not None:
        return (f"Deze zaak betreft een civiele {request.zaak.zaakstroom}zaak met {vw_desc}. "
                f"De partij is een {effective_type} in de rol van {request.partij.rol}. "
                f"Tariefcategorie: '{category}'. Griffierecht: €{amount}.")
    if outcome.get("manualReviewRequired"):
        return f"Civiele {request.zaak.zaakstroom}zaak. {effective_type}, rol: {request.partij.rol}. {outcome.get('manualReviewReason', 'Handmatige controle vereist.')}"
    return f"Civiele {request.zaak.zaakstroom}zaak. {effective_type}, rol: {request.partij.rol}. Geen griffierecht verschuldigd."


def calculate_calculation_id(request: CalculateRequest, ruleset_version: str) -> str:
    request_str = request.model_dump_json()
    return f"calc-{hashlib.sha256(f'{request_str}|{ruleset_version}'.encode()).hexdigest()[:16]}"


def compute_hash(data: str) -> str:
    return f"sha256:{hashlib.sha256(data.encode()).hexdigest()}"


# ─── Juridische Context ───

def build_juridische_context(jrem: dict) -> dict | None:
    """Build juridischeContext from JREM metadata."""
    metadata = jrem.get("metadata", {})
    jur_context = metadata.get("juridischeContext")
    if not jur_context:
        return None
    result = dict(jur_context)
    # Check wetVersieLaatstGecheckt < 1 jaar
    last_check = jur_context.get("wetVersieLaatstGecheckt")
    if last_check:
        try:
            check_date = datetime.fromisoformat(last_check)
            if (datetime.now(timezone.utc) - check_date.replace(tzinfo=timezone.utc)).days > 365:
                result["_bronverificatieWarning"] = "Bronverificatie is meer dan 1 jaar geleden — hercontroleer de wetstekst."
        except Exception:
            pass
    return result


# ─── Audit Store ───

_audit_store: dict[str, dict] = {}

def store_audit(calculation_id: str, request: CalculateRequest, response_data: dict, ruleset_hash: str):
    _audit_store[calculation_id] = {
        "calculationId": calculation_id,
        "inputHash": compute_hash(request.model_dump_json()),
        "rulesetHash": ruleset_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "response": response_data,
    }


# ─── Factory ───

def create_app(domain: str, jrem_dir: Path, port: int, endpoint_prefix: str = None) -> FastAPI:
    """
    Factory: create a FastAPI instance for a specific legal domain.
    
    Args:
        domain: "griffierecht", "procesreglement", "classificatie", etc.
        jrem_dir: Path to the JREM exports directory for this domain
        port: Port to bind (127.0.0.1 only)
        endpoint_prefix: URL prefix (defaults to /v1/{domain})
    """
    prefix = endpoint_prefix or f"/v1/{domain}"
    
    app = FastAPI(
        title=f"{domain.title()} Rule API",
        description=f"Auditbare juridische rule service voor {domain}",
        version="1.0.0",
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    @app.get("/v1/health")
    def health():
        try:
            versions = list_versions(jrem_dir)
        except Exception as e:
            return {"status": "degraded", "error": str(e), "domain": domain}
        return {"status": "ok", "service": f"{domain}-rule-api", "version": "1.0.0", "domain": domain, "rulesetVersions": versions}

    @app.get(f"{prefix}/versions")
    def get_versions():
        return {"versions": list_versions(jrem_dir)}

    @app.get("/v1/rules/{rule_id}")
    def get_rule(rule_id: str):
        for filepath in jrem_dir.glob("*.json"):
            with open(filepath) as f:
                data = json.load(f)
            for rule in data.get("rules", []):
                if rule["ruleId"] == rule_id:
                    return {"rule": rule, "rulesetVersion": data["version"], "validFrom": data["validFrom"], "validUntil": data["validUntil"]}
        raise HTTPException(status_code=404, detail=f"Rule {rule_id} not found")

    @app.post(f"{prefix}/calculate")
    def calculate(request: CalculateRequest):
        # Out-of-scope check
        if request.zaak.rechtsgebied != "civiel":
            return {
                "calculationId": calculate_calculation_id(request, "n/a"),
                "ruleSetVersion": "n/a", "domain": domain,
                "result": {"griffierecht": {"amount": None, "currency": "EUR"}, "category": "out_of_scope", "verschuldigdDoor": None, "manualReviewRequired": True},
                "explanation": {"summary": f"Rechtsgebied '{request.zaak.rechtsgebied}' is niet in scope.", "reasoningSteps": [f"Rechtsgebied is {request.zaak.rechtsgebied} → niet in scope"], "appliedRules": [], "sourceRefs": []},
                "warnings": ["niet in scope voor PoC: alleen civiele dagvaardingszaken"],
                "juridischeContext": None,
                "audit": {"inputHash": compute_hash(request.model_dump_json()), "rulesetHash": "n/a", "timestamp": datetime.now(timezone.utc).isoformat()},
            }

        # Select JREM version
        try:
            version = select_version(jrem_dir, request.calculationDate, request.tariefjaar)
            jrem = load_jrem(jrem_dir, version)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"JREM load failure: {e}")

        ruleset_str = json.dumps(jrem, sort_keys=True, ensure_ascii=False)
        ruleset_hash = compute_hash(ruleset_str)

        # Match rules (sorted by priority descending, first-match)
        sorted_rules = sorted(jrem["rules"], key=lambda r: r.get("priority", 0), reverse=True)
        matched_rule = None
        for rule in sorted_rules:
            if match_rule(rule, request):
                matched_rule = rule
                break

        if matched_rule is None:
            return {
                "calculationId": calculate_calculation_id(request, version), "ruleSetVersion": jrem["version"], "domain": domain,
                "result": {"griffierecht": {"amount": None, "currency": "EUR"}, "category": "no_match", "verschuldigdDoor": None, "manualReviewRequired": True},
                "explanation": {"summary": "Geen passende regel gevonden. Handmatige controle vereist.", "reasoningSteps": ["Geen regel gevonden"], "appliedRules": [], "sourceRefs": []},
                "warnings": ["Geen passende regel — verifieer input of raadpleeg een jurist"],
                "juridischeContext": build_juridische_context(jrem),
                "audit": {"inputHash": compute_hash(request.model_dump_json()), "rulesetHash": ruleset_hash, "timestamp": datetime.now(timezone.utc).isoformat()},
            }

        outcome = matched_rule["outcome"]
        amount = outcome.get("griffierecht", {}).get("amount")
        verschuldigd_door = request.partij.rol if amount is not None else None
        reasoning_steps = build_reasoning_steps(matched_rule, request)
        summary = build_summary(matched_rule, request)
        source_refs = [{"type": ref.get("type"), "title": ref.get("title"), "section": ref.get("section"), "url": ref.get("url")} for ref in matched_rule.get("sourceRefs", [])]
        warnings = []
        if outcome.get("manualReviewRequired"):
            warnings.append(outcome.get("manualReviewReason", "Handmatige controle vereist"))
        for tr in jrem.get("transitionRules", []):
            try:
                eff = datetime.fromisoformat(tr["effectiveDate"])
                calc = datetime.fromisoformat(request.calculationDate[:10])
                if abs((calc - eff).days) <= 30: warnings.append(f"Versie-overgang: {tr['description']}")
            except Exception: pass

        jur_ctx = build_juridische_context(jrem)
        if jur_ctx and jur_ctx.get("_bronverificatieWarning"):
            warnings.append(jur_ctx.pop("_bronverificatieWarning"))

        response_data = {
            "calculationId": calculate_calculation_id(request, version), "ruleSetVersion": jrem["version"], "domain": domain,
            "result": {"griffierecht": {"amount": amount, "currency": "EUR"} if amount is not None else {"amount": None, "currency": "EUR"}, "category": outcome.get("category", "onbekend"), "verschuldigdDoor": verschuldigd_door, "manualReviewRequired": outcome.get("manualReviewRequired", False)},
            "explanation": {"summary": summary, "reasoningSteps": reasoning_steps, "appliedRules": [matched_rule["ruleId"]], "sourceRefs": source_refs},
            "warnings": warnings,
            "juridischeContext": jur_ctx,
            "audit": {"inputHash": compute_hash(request.model_dump_json()), "rulesetHash": ruleset_hash, "timestamp": datetime.now(timezone.utc).isoformat()},
        }
        store_audit(response_data["calculationId"], request, response_data, ruleset_hash)
        return response_data

    @app.get("/v1/audit/{calculation_id}")
    def get_audit(calculation_id: str):
        if calculation_id not in _audit_store:
            raise HTTPException(status_code=404, detail=f"Calculation {calculation_id} not found")
        return _audit_store[calculation_id]

    return app
