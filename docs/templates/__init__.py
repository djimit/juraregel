"""JuraRegel Document Templates — Alle verplichte documenten.

Importeer en gebruik:
    from docs.templates import generate_document

    dpia = generate_document("dpia", "Gemeente Voorbeeld", verwerking="WOZ-verwerking")
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
}


def generate_document(doc_type: str, org_naam: str, **kwargs) -> dict:
    """Genereer een document op basis van type en organisatienaam."""
    template_func = TEMPLATES.get(doc_type)
    if not template_func:
        return {
            "error": f"Onbekend documenttype: {doc_type}",
            "available": list(TEMPLATES.keys()),
        }
    return template_func(org_naam, **kwargs)


def list_documents() -> list[dict]:
    """Lijst alle beschikbare documenten."""
    return [
        {"id": doc_id, "generator": func.__name__} for doc_id, func in TEMPLATES.items()
    ]
