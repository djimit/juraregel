# JuraRegel Use Cases — Volledig Overzicht

## Platform Use Cases (nieuw in v2.0)

### Compliance Orchestrator

**Als** compliance officer **wil ik** één API-call die een volledige compliance-assessment uitvoert **zodat** ik niet handmatig 7 verschillende modules hoef aan te roepen.

| Stap | Module | Beschrijting | Status |
|------|--------|-------------|--------|
| 1 | Multi-Jurisdiction | Bepaal toepasselijke frameworks | ✅ |
| 2 | Risk Prediction | Voorspel compliance risico's | ✅ |
| 3 | Knowledge Graph | Analyseer concept-relaties | ✅ |
| 4 | Drift Detection | Detecteer compliance-afwijkingen | ✅ |
| 5 | RAG Search | Zoek relevante juridische bronnen | ✅ |
| 6 | Synthese | Genereer conclusie (LLM of template) | ✅ |
| 7 | Audit Logging | Leg vast in audit trail | ✅ |

**API:**
```bash
POST /api/v1/orchestrator/assess
{
  "organisation_id": "gemeente-x",
  "processing_activity": {
    "name": "WOZ-AI",
    "ai_systems": true,
    "data_categories": ["Naam", "WOZ-waarde"],
    "data_subjects": ["Eigenaren"],
    "data_subject_count": 10000
  }
}
```

### Report Generator

**Als** privacy officer **wil ik** een volledig DPIA-document genereren **zodat** ik niet handmatig een DPIA hoef op te stellen.

| Rapport Type | Framework | Output |
|--------------|-----------|--------|
| DPIA | AVG Art. 35 | Markdown/PDF |
| FRIA | EU AI Act Art. 27 | Markdown/PDF |
| IAMA | Handvest Rechten van de Mens | Markdown/PDF |
| Compliance Verklaring | AVG + EU AI Act | Markdown/PDF |

**API:**
```bash
POST /api/v1/reports/generate/markdown
{
  "report_type": "dpia",
  "organisation": "Gemeente Voorbeeld",
  "processing_activity": { ... }
}
```

### Legal Reasoning Engine

**Als** jurist **wil ik** juridische argumentatie met bron-citaties **zodat** ik niet handmatig argumenten hoef te formuleren.

Gebruikt het Toulmin argumentatie model:
- **Claim** — De bewering
- **Grounds** — Feiten/bronnen
- **Warrant** — Regel/logica
- **Backing** — Onderbouwende bronnen
- **Qualifier** — Zekerheidsniveau
- **Rebuttal** — Tegenargumenten

### Predictive Compliance

**Als** CISO **wil ik** risico's voorspellen vóórdat ze optreden **zodat** ik preventief maatregelen kan nemen.

Features:
- 6 risico-factors met trigger-based probability
- Trend-analyse (improving/stable/declining)
- 30/90/180-dagen forecasts
- Early warning system
- Priority acties

### Continuous Evaluation

**Als** architect **wil ik** continu meten of het platform voldoet aan OpenMythos criteria **zodat** ik regressies direct zie.

| Module | Checks | Score |
|--------|--------|-------|
| RAG Engine | 4 | 100% |
| Legal Reasoning | 4 | 100% |
| Predictive Compliance | 4 | 100% |
| Report Generator | 4 | 100% |
| Accountable AI | 4 | 100% |
| Orchestrator | 4 | 100% |

**Overall: Grade A (100%)**

### Digital Twin

**Als** compliance officer **wil ik** "wat-if" scenario's simuleren **zodat** ik de impact van wijzigingen kan voorspellen.

Scenario's:
- Implementeer encryptie → +15 AVG score
- Voer DPIA uit → +20 AVG score
- Implementeer human oversight → +25 AI Act score

## Bestaande Use Cases (JREM Rule APIs)

| Use Case | Regels | Status | Poort |
|----------|--------|--------|-------|
| Griffierecht | 36 | **PoC** | 8490 |
| BIO2 | 162 | **PoC** | 8494 |
| Forum Standaardisatie | 22 | **PoC** | 8495 |
| Overheidsstandaarden | 24 | **PoC** | 8496 |
| NORA | 15 | **PoC** | 8497 |
| EU AI Act | 12 | PoC | 8498 |
| AVG/GDPR | 10 | PoC | 8499 |
| NCSC | 32 | PoC | 8500 |
| Judicial AI Assurance | 12 | **PoC, catalog-only** | 8521 |
| eIDAS 2.0 | 32 | PoC | 8523 |
| ... | ... | ... | ... |

## Architectuur Relaties

```
Bronnen → Data & AI → Core Platform → Analysis → Output → Consumers
```

Zie [README.md](../README.md) voor het volledige Mermaid diagram.
