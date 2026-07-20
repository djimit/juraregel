"""JuraRegel Document Templates — Alle verplichte documenten.

Importeer en gebruik:
    from docs.templates import generate_document, enrich_document, validate_document
    from docs.templates.render_engine import render_document
    from docs.templates.conditional_logic import ConditionalForm
    from docs.templates.evidence_linking import EvidenceLinker, AuditTrail
    from docs.templates.version_control import DocumentVersion, ApprovalWorkflow
    from docs.templates.i18n import translate, set_language

    dpia = generate_document("dpia", "Gemeente Voorbeeld", verwerking="WOZ-verwerking")
    enriched = enrich_document(dpia)
    md = render_document("dpia", "Gemeente Voorbeeld", format="markdown")
"""

from .privacy import (
    dpia_template,
    privacyverklaring_template,
    verwerkersovereenkomst_template,
    rova_template,
    datalek_procedure_template,
    toestemmingsregister_template,
)
from .informatiebeveiliging import (
    ib_beleid_template,
    statement_of_applicability_template,
    risicoanalyse_template,
    bcp_template,
    incident_response_template,
)
from .ai_algoritmes import (
    fria_template,
    algoritmeregister_template,
    technische_documentatie_ai_template,
)
from .overige import (
    nis2_cybersecurity_template,
    kwaliteitsbeleid_template,
    milieubeleid_template,
    arbobeleid_template,
    zorg_ib_beleid_template,
)
from .iama_fria_dpia import (
    dpia_rijksdienst_template,
    iama_template,
    fria_eu_template,
)
from .assessments_extended import (
    dpia_pre_scan_template,
    legitimate_interest_assessment_template,
    transfer_impact_assessment_template,
    ai_risicoclassificatie_template,
    privacy_by_design_checklist_template,
)
from .assessments_fase2 import (
    dpia_fria_overlap_matrix_template,
    kwantitatieve_risico_methodiek_template,
    bias_audit_protocol_template,
    human_oversight_plan_template,
    bewaarbeleid_template,
)
from .assessments_fase3 import (
    ethics_by_design_framework_template,
    value_sensitive_design_protocol_template,
    nist_ai_rmf_mapping_template,
    stakeholder_consultatie_protocol_template,
    dpia_review_protocol_template,
)
from .template_schema import validate_template, enrich_metadata, get_template_info

# ─── Template registry ──────────────────────────────────────

TEMPLATES = {
    # Privacy
    "dpia": dpia_template,
    "privacyverklaring": privacyverklaring_template,
    "verwerkersovereenkomst": verwerkersovereenkomst_template,
    "rova": rova_template,
    "datalek_procedure": datalek_procedure_template,
    "toestemmingsregister": toestemmingsregister_template,
    # Informatiebeveiliging
    "ib_beleid": ib_beleid_template,
    "statement_of_applicability": statement_of_applicability_template,
    "risicoanalyse": risicoanalyse_template,
    "bcp": bcp_template,
    "incident_response": incident_response_template,
    # AI & Algoritmes
    "fria": fria_template,
    "algoritmeregister": algoritmeregister_template,
    "technische_documentatie_ai": technische_documentatie_ai_template,
    # Overige
    "nis2_cybersecurity": nis2_cybersecurity_template,
    "kwaliteitsbeleid": kwaliteitsbeleid_template,
    "milieubeleid": milieubeleid_template,
    "arbobeleid": arbobeleid_template,
    "zorg_ib_beleid": zorg_ib_beleid_template,
    # Gedetailleerde assessments
    "dpia_rijksdienst": dpia_rijksdienst_template,
    "iama": iama_template,
    "fria_eu": fria_eu_template,
    # Fase 1 — Wettelijk kritieke assessments
    "dpia_pre_scan": dpia_pre_scan_template,
    "lia": legitimate_interest_assessment_template,
    "tia": transfer_impact_assessment_template,
    "ai_risicoclassificatie": ai_risicoclassificatie_template,
    "privacy_by_design": privacy_by_design_checklist_template,
    # Fase 2 — Methodologisch rijke assessments
    "dpia_fria_overlap": dpia_fria_overlap_matrix_template,
    "risico_methodiek": kwantitatieve_risico_methodiek_template,
    "bias_audit": bias_audit_protocol_template,
    "human_oversight": human_oversight_plan_template,
    "bewaarbeleid": bewaarbeleid_template,
    # Fase 3 — Academisch diep
    "ethics_by_design": ethics_by_design_framework_template,
    "value_sensitive_design": value_sensitive_design_protocol_template,
    "nist_ai_rmf": nist_ai_rmf_mapping_template,
    "stakeholder_consultatie": stakeholder_consultatie_protocol_template,
    "dpia_review": dpia_review_protocol_template,
}


def generate_document(doc_type: str, org_naam: str, **kwargs) -> dict:
    """Genereer een document op basis van type en organisatienaam.

    Auto-supplies defaults for templates that require extra arguments:
    - verwerking, ai_systeem, systeem, algoritme, belang,
      ontvanger_land, ontvanger_naam, verwerker
    """
    template_func = TEMPLATES.get(doc_type)
    if not template_func:
        return {
            "error": f"Onbekend documenttype: {doc_type}",
            "available": list(TEMPLATES.keys()),
        }
    defaults = {
        "verwerking": kwargs.get("verwerking", "[verwerking]"),
        "ai_systeem": kwargs.get("ai_systeem", "[AI-systeem]"),
        "systeem": kwargs.get("systeem", "[systeem]"),
        "algoritme": kwargs.get("algoritme", "[algoritme]"),
        "belang": kwargs.get("belang", "[belang]"),
        "ontvanger_land": kwargs.get("ontvanger_land", "[land]"),
        "ontvanger_naam": kwargs.get("ontvanger_naam", "[ontvanger]"),
        "verwerker": kwargs.get("verwerker", "[verwerker]"),
    }
    merged = {**defaults, **kwargs}
    return template_func(org_naam, **merged)


def enrich_document(doc: dict) -> dict:
    """Verrijk een document met standaard metadata (datum, model_versie, etc.)."""
    return enrich_metadata(doc)


def validate_document(doc: dict) -> dict:
    """Valideer dat een document voldoet aan het JuraRegel template schema."""
    return validate_template(doc)


def list_documents() -> list[dict]:
    """Lijst alle beschikbare documenten."""
    return [
        {"id": doc_id, "generator": func.__name__} for doc_id, func in TEMPLATES.items()
    ]


def get_document_info(doc_type: str, org_naam: str = "Organisatie", **kwargs) -> dict:
    """Haal metadata-info over een document type."""
    doc = generate_document(doc_type, org_naam, **kwargs)
    if "error" in doc:
        return doc
    enriched = enrich_document(doc)
    return get_template_info(enriched)
