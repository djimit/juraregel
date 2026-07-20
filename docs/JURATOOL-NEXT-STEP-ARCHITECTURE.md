# JuraRegel Next-Step Architecture — Van Document Generator naar Living Compliance Engine

**Versie:** 2.0 (2026-07-20)
**Status:** Strategisch architectuurdocument
**Niveau:** PhD-niveau productarchitectuur

---

## 0. Executive Summary

JuraRegel heeft een solide basis: 37 templates, traceability engine, 50+ use-cases. Maar de architectuur is nog **document-gecentreerd** — niet **compliance-gecentreerd**. De next step is de transformatie van een *document generator* naar een *living compliance engine* die:

1. **Continu monitort** of verwerkingen conform zijn vastgelegde assessments
2. **Automatisch detecteert** wetswijzigingen die impact hebben op bestaande verwerkingen
3. **AI-gestuurde analyse** biedt voor complexe compliance-vraagstukken
4. **Real-time compliance-postuur** toont per organisatie
5. **API-first** beschikbaar is voor integratie met externe systemen
6. **Multi-tenant** werkt voor meerdere organisaties met strikte scheiding

---

## 1. Huidige Architectuur — Analyse

### 1.1 Wat werkt (sterke punten)

| Component | Status | Waarde |
|-----------|--------|--------|
| Traceability Engine | ✅ Productie | Wet → Regel → Code → Test → Audit |
| JREM Exports | ✅ Productie | 50+ domeinen met gestructureerde regels |
| Template System | ✅ Productie | 37 templates met schema-validatie |
| Render Engine | ✅ Productie | Markdown/HTML/JSON output |
| CI/CD Gates | ✅ Productie | Automatische kwaliteitscontroles |
| Conditional Logic | ✅ Productie | Interactieve invul-flows |
| Evidence Linking | ✅ Productie | Bewijsstukken gekoppeld aan secties |

### 1.2 Wat ontbreekt (kritieke gaps)

| Gap | Ernst | Impact |
|-----|-------|--------|
| **Geen continue monitoring** | 🔴 Kritiek | DPIA is een momentopname, geen continue compliance |
| **Geen wetswijzigingsdetectie** | 🔴 Kritiek | Wijzigingen in wetgeving worden niet automatisch gedetecteerd |
| **Geen AI-gestuurde analyse** | 🔴 Kritiek | Geen LLM-interpretatie van wetgeving of risico-beoordeling |
| **Geen real-time dashboard** | 🟠 Hoog | Geen zicht in compliance-postuur op elk moment |
| **Geen API voor tooling** | 🟠 Hoog | Templates zijn Python-only, geen REST interface |
| **Geen multi-tenancy** | 🟠 Hoog | Geen scheiding tussen organisaties |
| **Geen notificaties** | 🟠 Hoog | Geen alerts bij veranderingen of deadlines |
| **Geen integratie externe bronnen** | 🟡 Middel | Geen koppeling BRP, BAG, DigiD, eHerkenning |
| **Geen compliance scoring** | 🟡 Middel | Geen kwantitatieve compliance-score |
| **Geen workflow engine** | 🟡 Middel | Geen proces-automatisering rond assessments |

---

## 2. Toekomstige Architectuur — Living Compliance Engine

### 2.1 Architectuur-visie

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        JURATOOL PLATFORM                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Regulatory  │  │  Compliance │  │    Risk     │  │   Audit     │   │
│  │  Monitoring  │  │   Engine    │  │   Engine    │  │   Trail     │   │
│  │  Service     │  │             │  │             │  │   Service   │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │                │            │
│  ┌──────┴────────────────┴────────────────┴────────────────┴──────┐    │
│  │                      API GATEWAY (REST + GraphQL)               │    │
│  └──────────────────────────────┬─────────────────────────────────┘    │
│                                 │                                       │
│  ┌──────────────────────────────┴─────────────────────────────────┐    │
│  │                    CORE SERVICES LAYER                         │    │
│  │                                                                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │    │
│  │  │ Template │ │ Evidence │ │ Version  │ │ Workflow │         │    │
│  │  │ Service  │ │ Service  │ │ Control  │ │ Engine   │         │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │    │
│  │  │  Render  │ │  i18n    │ │ Conditional│ │  Schema  │         │    │
│  │  │  Engine  │ │  Service │ │  Logic   │ │ Validator│         │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                 │                                       │
│  ┌──────────────────────────────┴─────────────────────────────────┐    │
│  │                      AI / LLM LAYER                            │    │
│  │                                                                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │    │
│  │  │  Legal   │ │  Risk    │ │ Regulatory│ │  Bias     │         │    │
│  │  │  Reasoning│ │ Predictor│ │  Change   │ │ Detector │         │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                 │                                       │
│  ┌──────────────────────────────┴─────────────────────────────────┐    │
│  │                    DATA LAYER                                  │    │
│  │                                                                │    │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │    │
│  │  │Processing│ │ Assessment│ │ Regulatory│ │  Audit   │         │    │
│  │  │ Register │ │ Store    │ │  Corpus   │ │  Store   │         │    │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Kern-componenten

#### A. Regulatory Monitoring Service

**Doel:** Continu monitoren van wetswijzigingen die impact hebben op geregistreerde verwerkingen.

**Functionaliteit:**
- Dagelijkse scraping van officiële bronnen (Staatsblad, Staatscourant, EUR-Lex, EDPB)
- NLP-gestuurde analyse van wijzigingen (impact-score per wijziging)
- Automatische koppeling tussen wijzigingen en geraakte verwerkingen
- Notificaties bij hoge-impact wijzigingen
- Integratie met bestaande traceability engine

**Bronnen:**
- Staatsblad: https://www.officielebekendmakingen.nl/
- EUR-Lex: https://eur-lex.europa.eu/
- EDPB: https://edpb.europa.eu/
- AP: https://www.autoriteitpersoonsgegevens.nl/
- EU AI Office: https://digital-strategy.ec.europa.eu/

**Technische implementatie:**
```python
class RegulatoryMonitor:
    def scan_sources(self) -> list[RegulatoryChange]
    def analyze_impact(self, change: RegulatoryChange) -> ImpactScore
    def notify_affected(self, change: RegulatoryChange) -> list[Notification]
    def link_to_assessments(self, change: RegulatoryChange) -> list[Assessment]
```

#### B. Compliance Engine

**Doel:** Continue beoordelen of verwerkingen conform zijn vastgelegde assessments.

**Functionaliteit:**
- Periodieke her-evaluatie van DPIA's, FRIA's, IAMA's
- Automatische detectie van afwijkingen (drift detection)
- Compliance scoring per verwerking (0-100)
- Trend-analyse over tijd
- Integratie met data-catalogus (wat wordt er werkelijk verwerkt?)

**Compliance Score Model:**
```
Compliance Score = Σ(wi × si) / Σ(wi)

Waarbij:
- wi = weight per criterium
- si = score per criterium (0-1)

Criterien:
- Documentatie compleet (20%)
- Evidence bijgewerkt (15%)
- Review-termijnen gehaald (15%)
- Maatregelen geïmplementeerd (20%)
- Incidenten afgehandeld (10%)
- Training actueel (10%)
- Stakeholder-consultatie (10%)
```

#### C. Risk Engine

**Doel:** AI-gestuurde risico-analyse en voorspelling.

**Functionaliteit:**
- Risico-scoring op basis van historische data
- Voorspellende analyse (welke risico's nemen toe?)
- Scenario-analyse (wat als wetgeving wijzigt?)
- Benchmark tegen vergelijkbare organisaties
- Integratie met externe threat intelligence

#### D. Workflow Engine

**Doel:** Proces-automatisering rond compliance-activiteiten.

**Functionaliteit:**
- Assessment-workflows (aanmaken → review → goedkeuren → publiceren)
- Review-cycles (plannen → uitvoeren → rapporteren → bijwerken)
- Escalatie-procedures (deadline dreigt → escalatie naar management)
- Notificatie-workflows (e-mail, Slack, Teams)
- Integratie met BPMN 2.0 voor complexe processen

**Workflow Templates:**
1. **DPIA Lifecycle:** Initiatief → Pre-scan → Volledige DPIA → Review → Goedkeuring → Publicatie → Monitoring → Herziening
2. **FRIA Lifecycle:** Classificatie → Impact Assessment → Mitigatie → Goedkeuring → Monitoring → Update
3. **Incident Response:** Detectie → Containment → Eradicatie → Herstel → Lessons Learned → Update Procedures
4. **Regulatory Change:** Detectie → Impact Analyse → Stakeholder Consultatie → Aanpassing → Validatie → Implementatie

---

## 3. Data Model — Next Generation

### 3.1 Entiteiten

```python
@dataclass
class Organisation:
    id: str
    name: str
    sector: str  # overheid, zorg, finance, etc.
    size: int  # aantal medewerkers
    contact: Contact
    created: datetime
    compliance_frameworks: list[str]  # AVG, AI Act, ISO 27001, etc.

@dataclass
class ProcessingActivity:
    id: str
    organisation_id: str
    name: str
    purpose: str
    legal_basis: str  # AVG Art. 6(1)(a-f)
    data_categories: list[str]
    data_subjects: list[str]
    recipients: list[str]
    retention_period: str
    security_measures: list[str]
    dpia_required: bool
    dpia_id: str | None
    fria_required: bool
    fria_id: str | None
    status: str  # active, paused, terminated
    created: datetime
    updated: datetime

@dataclass
class Assessment:
    id: str
    organisation_id: str
    processing_activity_id: str
    assessment_type: str  # dpia, fria, iama, lia, tia, bias_audit
    template_version: str
    status: str  # draft, in_review, approved, published, archived
    content: dict  # Template output
    evidence: list[Evidence]
    approvals: list[Approval]
    compliance_score: float  # 0-100
    next_review_date: datetime
    created: datetime
    updated: datetime

@dataclass
class Evidence:
    id: str
    assessment_id: str
    evidence_type: str  # wetgeving, beleid, audit, certificaat
    title: str
    reference: str  # URL of document-ID
    verified_by: str
    verified_at: datetime
    expiry_date: datetime | None
    status: str  # active, expired, superseded

@dataclass
class RegulatoryChange:
    id: str
    source: str  # EUR-Lex, Staatsblad, EDPB, etc.
    title: str
    summary: str
    effective_date: datetime
    impact_score: float  # 0-1
    affected_frameworks: list[str]
    affected_processing_activities: list[str]
    status: str  # detected, analyzed, action_required, resolved
    detected_at: datetime
    resolved_at: datetime | None

@dataclass
class ComplianceIncident:
    id: str
    organisation_id: str
    processing_activity_id: str
    incident_type: str  # datalek, bias_detectie, non-conformity
    severity: str  # low, medium, high, critical
    description: str
    measures_taken: list[str]
    notification_required: bool
    notification_sent: bool
    status: str  # open, contained, resolved, closed
    detected_at: datetime
    resolved_at: datetime | None
```

### 3.2 Relaties

```
Organisation 1:N ProcessingActivity
Organisation 1:N Assessment
Organisation 1:N ComplianceIncident
ProcessingActivity 1:1 Assessment (per type)
Assessment 1:N Evidence
Assessment 1:N Approval
RegulatoryChange N:M ProcessingActivity
RegulatoryChange N:M Assessment
ProcessingActivity 1:N ComplianceIncident
```

---

## 4. API Design — REST + GraphQL

### 4.1 REST Endpoints

```
/api/v1/
├── /organisations
│   ├── GET    /                    # Lijst organisaties
│   ├── POST   /                    # Maak organisatie aan
│   ├── GET    /{id}                # Haal organisatie op
│   ├── PUT    /{id}                # Update organisatie
│   └── DELETE /{id}                # Verwijder organisatie
│
├── /processing-activities
│   ├── GET    /                    # Lijst verwerkingen
│   ├── POST   /                    # Maak verwerking aan
│   ├── GET    /{id}                # Haal verwerking op
│   ├── PUT    /{id}                # Update verwerking
│   ├── DELETE /{id}                # Verwijder verwerking
│   └── GET    /{id}/compliance     # Compliance status
│
├── /assessments
│   ├── GET    /                    # Lijst assessments
│   ├── POST   /                    # Maak assessment aan
│   ├── GET    /{id}                # Haal assessment op
│   ├── PUT    /{id}                # Update assessment
│   ├── POST   /{id}/approve        # Keur goed
│   ├── POST   /{id}/publish        # Publiceer
│   ├── POST   /{id}/archive        # Archiveer
│   ├── GET    /{id}/evidence       # Haal evidence op
│   ├── POST   /{id}/evidence       # Voeg evidence toe
│   └── GET    /{id}/export         # Exporteer (PDF, Word, JSON)
│
├── /templates
│   ├── GET    /                    # Lijst templates
│   ├── GET    /{id}                # Haal template op
│   ├── POST   /{id}/generate       # Genereer document
│   └── POST   /{id}/validate       # Valideer invulling
│
├── /regulatory-changes
│   ├── GET    /                    # Lijst wijzigingen
│   ├── GET    /{id}                # Haal wijziging op
│   ├── GET    /{id}/impact         # Impact-analyse
│   └── POST   /{id}/resolve        # Markeer opgelost
│
├── /compliance-score
│   ├── GET    /{org_id}            # Organisatie score
│   ├── GET    /{org_id}/trend      # Trend over tijd
│   └── GET    /{org_id}/benchmark  # Vergelijking sector
│
└── /audit-trail
    ├── GET    /                    # Lijst audit entries
    └── GET    /{entity_id}          # Entiteit geschiedenis
```

### 4.2 GraphQL Schema

```graphql
type Organisation {
  id: ID!
  name: String!
  sector: String!
  processingActivities: [ProcessingActivity!]!
  assessments(filter: AssessmentFilter): [Assessment!]!
  complianceScore: ComplianceScore!
  incidents(status: IncidentStatus): [ComplianceIncident!]!
}

type ProcessingActivity {
  id: ID!
  name: String!
  purpose: String!
  legalBasis: String!
  dpia: Assessment
  fria: Assessment
  complianceStatus: ComplianceStatus!
  lastAssessmentDate: DateTime
  nextReviewDate: DateTime
}

type Assessment {
  id: ID!
  type: AssessmentType!
  status: AssessmentStatus!
  content: JSON!
  evidence: [Evidence!]!
  complianceScore: Float
  approvals: [Approval!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type RegulatoryChange {
  id: ID!
  source: String!
  title: String!
  impactScore: Float!
  affectedActivities: [ProcessingActivity!]!
  status: ChangeStatus!
  detectedAt: DateTime!
}

type Query {
  organisation(id: ID!): Organisation
  processingActivity(id: ID!): ProcessingActivity
  assessment(id: ID!): Assessment
  regulatoryChanges(since: DateTime): [RegulatoryChange!]!
  complianceDashboard(organisationId: ID!): ComplianceDashboard!
}

type Mutation {
  createProcessingActivity(input: ProcessingActivityInput!): ProcessingActivity!
  submitAssessment(input: AssessmentInput!): Assessment!
  approveAssessment(id: ID!, approval: ApprovalInput!): Assessment!
  addEvidence(assessmentId: ID!, evidence: EvidenceInput!): Evidence!
  resolveChange(id: ID!): RegulatoryChange!
}

type Subscription {
  regulatoryChangeDetected: RegulatoryChange!
  complianceScoreChanged(organisationId: ID!): ComplianceScore!
  incidentDetected(organisationId: ID!): ComplianceIncident!
}
```

---

## 5. AI/LLM Integratie

### 5.1 Legal Reasoning Engine

**Doel:** AI-gestuurde interpretatie van wetgeving en compliance-beoordeling.

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│                 Legal Reasoning Engine                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Statute     │  │   Case Law   │  │  Regulatory  │  │
│  │   Analyzer    │  │   Analyzer   │  │  Guidance    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │            │
│  ┌──────┴─────────────────┴─────────────────┴──────┐    │
│  │              RAG Pipeline (Retrieval)            │    │
│  │                                                   │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │    │
│  │  │  Vector     │  │  Hybrid    │  │ Re-ranker  │ │    │
│  │  │  Store     │  │  Search    │  │            │ │    │
│  │  └────────────┘  └────────────┘  └────────────┘ │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐    │
│  │           LLM Inference Layer                     │    │
│  │                                                   │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │    │
│  │  │  Claude    │  │  GPT-4     │  │  Gemini    │ │    │
│  │  │  (Primary) │  │  (Fallback)│  │  (Review)  │ │    │
│  │  └────────────┘  └────────────┘  └────────────┘ │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐    │
│  │          Output Validation Layer                  │    │
│  │                                                   │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │    │
│  │  │  Citation  │  │  Hallucin. │  │  Confidence│ │    │
│  │  │  Checker   │  │  Detector  │  │  Scorer    │ │    │
│  │  └────────────┘  └────────────┘  └────────────┘ │    │
│  └───────────────────────────────────────────────────┘    │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 5.2 AI Use Cases

| Use Case | LLM Rol | Input | Output |
|----------|---------|-------|--------|
| **Wetgeving interpreteren** | Analyseer wettekst | Wetsartikel + context | Samenvatting + implicaties |
| **DPIA adviseren** | Beoordeel risico's | Verwerkingsbeschrijving | Risico-score + maatregelen |
| **FRIA analyseren** | Impact-analyse | AI-systeem beschrijving | Grondrechten-impact |
| **Regulatory change impact** | Impact-beoordeling | Wijziging + verwerkingen | Aanbevelingen |
| **Compliance vragen** | Q&A | Vraag + context | Antwoord + citaten |
| **Document genereren** | Template-vulling | Gegevens + template | Volledig document |
| **Bias detectie** | Data-analyse | Dataset + model | Bias-rapport |
| **Incident analyse** | Root cause analyse | Incident-data | Oorzaak + maatregelen |

### 5.3 RAG Pipeline

**Knowledge Sources:**
1. **Regulatory Corpus:** Alle EU- en NL-wetgeving (AVG, AI Act, etc.)
2. **Guidance Corpus:** EDPB richtlijnen, AP-uitspraken, EU AI Office guidance
3. **Case Law Corpus:** Relevante uitspraken (rechtbanken, HvJEU)
4. **Internal Corpus:** Organisatie-specifieke documenten, eerdere assessments
5. **Template Corpus:** Alle 37 JuraRegel templates + voorbeelden

**Vector Store:**
- Embedding model: `text-embedding-3-large` of `all-MiniLM-L6-v2` (local)
- Vector database: Qdrant (al beschikbaar op 192.168.1.28:6333)
- Chunking: Semantische chunking met overlap, gemarkeerd met bron-metadata

### 5.4 Hallucination Prevention

**Lagen van validatie:**
1. **Citation Checking:** Elke bewering moet een bron-citatie hebben
2. **Confidence Scoring:** LLM geeft confidence-score per bewering
3. **Human-in-the-loop:** Kritieke beweringen vereisen menselijke validatie
4. **Cross-referencing:** Controle tegen bekende feiten in knowledge base
5. **Audit Trail:** Alle AI-beweringen worden gelogd met bronvermelding

---

## 6. Multi-Tenant Architectuur

### 6.1 Tenant Isolation

```
┌─────────────────────────────────────────────────────────┐
│                    TENANT LAYER                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ Tenant A    │  │ Tenant B    │  │ Tenant C    │    │
│  │ Gemeente X  │  │ Zorgorg. Y  │  │ Ministerie Z│    │
│  │             │  │             │  │             │    │
│  │ • Eigen DB  │  │ • Eigen DB  │  │ • Eigen DB  │    │
│  │ • Eigen RBAC│  │ • Eigen RBAC│  │ • Eigen RBAC│    │
│  │ • Eigen cfg │  │ • Eigen cfg │  │ • Eigen cfg │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  Shared: Templates, Regulatory Corpus, AI Models        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Rollen en Rechten

| Rol | Permissies | Scope |
|-----|-----------|-------|
| **Super Admin** | Alles | Platform |
| **Tenant Admin** | Tenant-configuratie, gebruikers | Eigen tenant |
| **Functionaris Gegevensbescherming (FG)** | DPIA's goedkeuren, verwerkingen beheren | Eigen tenant |
| **AI-verantwoordelijke** | FRIA's goedkeuren, AI-register | Eigen tenant |
| **Compliance Officer** | Assessments maken, evidence toevoegen | Eigen tenant |
| **Auditor** | Alleen lezen, audit trail | Eigen tenant |
| **Management** | Dashboard, rapporten | Eigen tenant |
| **Externe Auditor** | Beperkte leestoegang | Eigen tenant + tijdsgebonden |

---

## 7. Implementatie Roadmap

### Fase 5: API-First (Maand 1-2)

| # | Component | Complexiteit | Deliverable |
|---|-----------|-------------|-------------|
| 5.1 | REST API voor templates | Medium | `/api/v1/templates/*` |
| 5.2 | REST API voor assessments | Medium | `/api/v1/assessments/*` |
| 5.3 | REST API voor processing activities | Medium | `/api/v1/processing-activities/*` |
| 5.4 | API authenticatie (OAuth2 + API keys) | Hoog | Auth layer |
| 5.5 | API rate limiting + throttling | Laag | Middleware |
| 5.6 | API documentatie (OpenAPI 3.1) | Laag | Swagger UI |

### Fase 6: Data Layer (Maand 2-3)

| # | Component | Complexiteit | Deliverable |
|---|-----------|-------------|-------------|
| 6.1 | PostgreSQL schema | Hoog | Migrations |
| 6.2 | Processing Activity register | Hoog | CRUD + search |
| 6.3 | Assessment store | Hoog | CRUD + versioning |
| 6.4 | Evidence store | Medium | Upload + verify |
| 6.5 | Audit trail store | Medium | Immutable log |
| 6.6 | Vector store setup (Qdrant) | Medium | Embeddings |

### Fase 7: AI Integration (Maand 3-4)

| # | Component | Complexiteit | Deliverable |
|---|-----------|-------------|-------------|
| 7.1 | RAG pipeline | Hoog | Retrieval service |
| 7.2 | Legal reasoning prompts | Hoog | Prompt library |
| 7.3 | Citation validation | Medium | Validator |
| 7.4 | Confidence scoring | Medium | Scorer |
| 7.5 | Hallucination detection | Hoog | Detector |
| 7.6 | AI-assisted DPIA generation | Hoog | AI-DPIA flow |

### Fase 8: Monitoring & Dashboard (Maand 4-5)

| # | Component | Complexiteit | Deliverable |
|---|-----------|-------------|-------------|
| 8.1 | Regulatory monitoring service | Hoog | Change detection |
| 8.2 | Compliance scoring engine | Hoog | Score model |
| 8.3 | Real-time dashboard | Hoog | React/Next.js UI |
| 8.4 | Notificatie service | Medium | E-mail + webhook |
| 8.5 | Reporting engine | Medium | PDF/Excel export |
| 8.6 | Benchmark engine | Medium | Sector Vergelijking |

### Fase 9: Workflow & Automation (Maand 5-6)

| # | Component | Complexiteit | Deliverable |
|---|-----------|-------------|-------------|
| 9.1 | Workflow engine | Hoog | BPMN 2.0 engine |
| 9.2 | Assessment workflows | Hoog | 4 lifecycle flows |
| 9.3 | Escalatie-automatisering | Medium | Escalation rules |
| 9.4 | Review-cycle planning | Medium | Scheduler |
| 9.5 | Integration connectors | Hoog | DigiD, eHerkenning, BRP |

---

## 8. Technische Stack — Aanbeveling

| Component | Huidige Stack | Aanbevolen Stack | Reden |
|-----------|--------------|------------------|-------|
| **Backend** | Python (scripts) | Python (FastAPI) | Async, OpenAPI, type-safe |
| **Frontend** | Static HTML | Next.js 15 (App Router) | React, SSR, API routes |
| **Database** | JSON files | PostgreSQL 16 | ACID, search, JSONB |
| **Vector Store** | Geen | Qdrant | Al beschikbaar, hybrid search |
| **Cache** | Geen | Redis | Sessions, rate limiting |
| **Message Queue** | Geen | Celery + Redis | Async tasks, scheduling |
| **LLM** | Geen | Claude (via LiteLLM) | Juridische reasoning |
| **Auth** | Geen | Keycloak | OAuth2, RBAC, multi-tenant |
| **Monitoring** | Geen | Prometheus + Grafana | Metrics, alerting |
| **CI/CD** | GitHub Actions | GitHub Actions (uitbreiden) | Bestaande infra |
| **Hosting** | Linux workstation | Kubernetes (k3s) | Scalability |

---

## 9. Compliance-by-Design Principes

### 9.1 Privacy by Default

- **Data minimalisatie:** Alleen verzamelen wat nodig is
- **Purpose limitation:** Data alleen gebruikt voor vastgelegd doel
- **Storage limitation:** Automatische verwijdering na bewaartermijn
- **Encryption:** At rest (AES-256) + in transit (TLS 1.3)
- **Access control:** RBAC + ABAC + need-to-know

### 9.2 Security by Design

- **Zero Trust:** Geen impliciete vertrouwensrelaties
- **Immutable audit trail:** Append-only logging
- **Encryption key management:** HSM of KMS
- **Penetration testing:** Jaarlijks + bij major changes
- **Incident response:** Geautomatiseerde detectie + escalatie

### 9.3 Explainability

- **AI-beweringen:** Altijd met bron-citatie
- **Compliance scores:** Transparante berekening
- **Aanbevelingen:** Onderbouwd met wetsartikelen
- **Audit trail:** Volledige herleidbaarheid

---

## 10. Conclusie — De Next Step

JuraRegel heeft een unieke positie: **de enige open-source compliance engine die vertrekt van juridische regels en deze vertaalt naar IT-uitvoering**. De next step is het combineren van:

1. **Bestaande kracht:** Traceability engine + 37 templates + 50+ use-cases
2. **Nieuwe AI-laag:** Legal reasoning, RAG, automated analysis
3. **Nieuwe data-laag:** PostgreSQL + Qdrant + real-time monitoring
4. **Nieuwe API-laag:** REST + GraphQL voor integratie
5. **Nieuwe UI-laag:** Real-time compliance dashboard

**Het resultaat:** Een platform dat niet alleen documenten genereert, maar **continue compliance garandeert** — van wetgeving tot implementatie, van assessment tot monitoring, van detectie tot remediatie.

Dit is de transformatie van **JuraRegel als tool** naar **JuraRegel als platform**.

---

*Gegenereerd: 2026-07-20*
*Auteur: JuraRegel Architectuur Team*
*Review: FG, AI-verantwoordelijke, CISO*
