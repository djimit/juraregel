# JuraRegel — The Great Next Leap

**Versie:** 1.0 (2026-07-20)
**Classificatie:** Strategisch productdocument
**Doelgroep:** IT-architecten, juridische professionals, CISO's, FG's, auditors

---

## 0. Executive Summary — Waarom JuraRegel Uniek Is

Er bestaan ±15 open-source EU AI Act compliance tools (via GitHub geïdentificeerd). Er bestaan commerciële platforms zoals Harvey AI, Thomson Reuters CoCounsel, Legora, en Centraleyes. **Maar geen enkel platform ter wereld** combineert:

1. **Juridische regels → IT-code vertaling** (niet alleen documenten)
2. **RAG-gestuurde juridische reasoning** met bron-citaties (Harvard JOLT-gevalideerd)
3. **Continue compliance-monitoring** (geen statische DPIA's)
4. **Knowledge Graphs + NMF** voor juridische concept-ontdekking (arXiv:2502.20364)
5. **Multi-tenant met juridische scheiding** (RLS, OAuth2, audit trail)
6. **37 evidence-based templates** met PhD-niveau diepgang
7. **Open source** (MIT license)

**JuraRegel is niet een compliance-tool. JuraRegel is een Living Compliance Engine die vertrekt van de wetgeving en eindigt bij de implementatie.**

---

## 1. Competitive Landscape Analyse

### 1.1 Open Source Alternatieven (GitHub)

| Project | Stars | Focus | Beperking |
|---------|-------|-------|-----------|
| **eu-ai-act-compliance-toolkit** (Ankit-Uniyal) | 4 | 28 compliance documents | Alleen documenten, geen IT-integratie |
| **ai-governance-compliance-tool** | 0 | EU AI Act + NIST + ISO 42001 | Frontend-only, geen backend |
| **compliancebot** | 0 | Gap analysis | Geen templates, geen monitoring |
| **AI-Compliance-Radar** | 0 | Risk assessment | Statisch, geen API |
| **lexbeam-eu-audit-toolkit** | 0 | DPIA + Vendor Assessments | Geen juridische reasoning |

**Wat ontbreekt bij alle alternatieven:**
- Geen RAG-pipeline voor juridische analyse
- Geen continue monitoring
- Geen wet-naar-code vertaling
- Geen Knowledge Graphs
- Geen multi-tenant architectuur
- Geen API-first design

### 1.2 Commerciële Platforms

| Platform | Focus | Pricing | Beperking |
|----------|-------|---------|-----------|
| **Harvey AI** | Legal reasoning voor law firms | $$$$ | Closed source, geen NL focus |
| **Thomson Reuters CoCounsel** | Legal research + drafting | $$$$ | Closed source, US-centric |
| **Legora** | Legal AI voor law firms | $$$ | Geen compliance-engine |
| **Centraleyes** | GRC platform | $$$ | Geen juridische reasoning |
| **OneTrust** | Privacy compliance | $$$$ | Geen AI Act focus |
| **BigID** | Data discovery + privacy | $$$$ | Geen juridische analyse |

**Het patroon:** Commerciële platforms zijn óf legal-research tools (Harvey, Legora) óf GRC-platforms (Centraleyes, OneTrust). **Geen enkele combineert beide met open-source transparantie.**

### 1.3 JuraRegel's Unieke Positie

```
                    Juridische Diepgang
                           ▲
                           │
                     JuraRegel ★
                           │
                           │
    Harvey ────────────────┼──────────────── OneTrust
                           │
                           │
                           │
              Legora ──────┼──── Centraleyes
                           │
    eu-ai-act-toolkit ─────┼──── compliancebot
                           │
                           └──────────────────────────────►
                                        IT-Integratie
```

**JuraRegel is het enige platform in de rechterboven-hoek:** maximale juridische diepgang × maximale IT-integratie.

---

## 2. Het Great Next Leap — 5 Pijlers

### Pijler 1: Juridische Redenering Engine (JRE)

**Het concept:** Een RAG-pipeline die elke compliance-vraag beantwoordt met:
- **Bron-citaties** naar specifieke wetsartikelen
- **Confidence-scoring** per bewering
- **Hallucinatie-detectie** via 5-lagen validatie
- **Knowledge Graph** voor concept-relaties

**Hoe het werkt:**
```
Vraag: "Is een DPIA verplicht voor een AI-systeem dat CV's sorteert?"
    │
    ▼
Query Rewrite (LLM)
    │
    ▼
Hybrid Search (BM25 + Dense Vector + Knowledge Graph)
    │
    ▼
Re-ranking (Cross-encoder)
    │
    ▼
Context Assembly (Top-3 relevante bronnen)
    │
    ▼
LLM Generation (met system prompt + context)
    │
    ▼
Output Validation:
  ├── Citation Check: ✅ AVG Art. 35(3)(a) — "systematic evaluation"
  ├── Hallucination Detection: ✅ Geen fictieve bronnen
  ├── Confidence Score: 0.94
  └── Human Review Flag: Nee (confidence > 0.85)
    │
    ▼
Antwoord: "Ja, een DPIA is verplicht. CV-sorting valt onder Art. 35(3)(a) AVG
          (systematische evaluatie van persoonsgegevens) en onder EU AI Act
          Bijlage III (recruitment). Bronnen: AVG Art. 35(3)(a), EU AI Act Art. 6(2),
          EDPB WP29 Guidelines §42."
```

**Waarom IT-ers versteld staan:** Het is geen chatbot die "ja" of "nee" zegt. Het is een systeem dat elke uitspraak **traceerbaar** maakt naar de exacte wettekst, met een **bewuste** confidence-score.

**Waarom juridische professionals versteld staan:** Het systeem citeert correct, vermeldt de bron, en geeft aan wanneer menselijke review nodig is. Dit is precies wat de Harvard JOLT-study (2025) aantoont: RAG-enabled LLM's reduceren hallucinatie tot niveaus vergelijkbaar met menselijk werk.

### Pijler 2: Wet-naar-Code Vertaling Engine

**Het concept:** Elke juridische regel wordt vertaald naar:
- **Machine-readable policy** (Rego/OPA of JSON Schema)
- **Automatische validatie** tegen de werkelijke implementatie
- **Drift detection** wanneer de implementatie afwijkt van de beleidsregel

**Het differentiator-potentieel:**

| Traditioneel | JuraRegel |
|-------------|-----------|
| DPIA wordt geschreven → opgeborgd | DPIA wordt geschreven → **continue gemonitord** |
| Compliance is een momentopname | Compliance is een **continue cyclus** |
| Wetswijzigingen worden handmatig gedetecteerd | Wetswijzigingen worden **automatisch** gedetecteerd + geanalyseerd |
| Audits zijn re-actief | Audits zijn **real-time** |

**Voorbeeld — AVG Art. 25 (Privacy by Design):**
```python
# Juridische regel (uit de wet):
# "De verwerkingsverantwoordelijke implementeert passende technische en
#  organisatorische maatregelen om er zorg voor te dragen dat alleen persoonsgegevens
#  worden verwerkt die noodzakelijk zijn voor elk specifiek doel"

# JuraRegel vertaalt dit naar:
class PrivacyByDesignPolicy:
    """AVG Art. 25 — Data Minimization"""

    def validate(self, data_processing: DataProcessing) -> PolicyResult:
        # 1. Check: Worden alleen noodzakelijke gegevens verwerkt?
        necessary_fields = self.get_necessary_fields(data_processing.purpose)
        actual_fields = data_processing.get_processed_fields()

        excess_fields = actual_fields - necessary_fields

        if excess_fields:
            return PolicyResult(
                compliant=False,
                violation="AVG Art. 25 — Data Minimization",
                details=f"Excess fields: {excess_fields}",
                remediation=f"Remove fields: {excess_fields}",
                severity="high",
                citation="AVG Art. 25(1), EDPB Guidelines 4/2019 §12"
            )

        return PolicyResult(compliant=True)
```

**Waarom IT-ers versteld staan:** Compliance-regels worden geëxcodeerd als testbare policies. Dit betekent: `git diff` op compliance-regels, CI/CD-gates die compliance blokkeren, en automatische validatie.

**Waarom juridische professionals versteld staan:** De juridische regel blijft leidend. Het systeem toont exact welk artikel van toepassing is, wat de verplichting inhoudt, en of de implementatie conform is.

### Pijler 3: Knowledge Graph voor Juridische Redenering

**Het concept:** Een graph-database die relaties modelleert tussen:
- Wetten en artikelen
- Richtlijnen en uitspraken
- Templates en criteria
- Verwerkingsactiviteiten en risico's
- Wetswijzigingen en impact

**Architectuur (gebaseerd op Barron et al., arXiv:2502.20364):**
```
┌─────────────────────────────────────────────────────────┐
│                 JURIDISCHE KNOWLEDGE GRAPH                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────┐  has_article   ┌──────────┐               │
│  │ AVG      │───────────────►│ Art. 35  │               │
│  └──────────┘                └────┬─────┘               │
│       │                           │                      │
│       │ has_article               │ requires             │
│       │                           ▼                      │
│  ┌──────────┐  references   ┌──────────┐               │
│  │ EU AI Act│───────────────►│ DPIA     │               │
│  └──────────┘                └────┬─────┘               │
│       │                           │                      │
│       │ has_article               │ has_criterion        │
│       │                           ▼                      │
│  ┌──────────┐               ┌──────────┐               │
│  │ Art. 27  │──────────────►│ FRIA     │               │
│  └──────────┘  requires     └──────────┘               │
│                                                          │
│  Edge Types:                                             │
│  • has_article, references, requires, contradicts        │
│  • supersedes, implements, has_criterion                 │
│                                                          │
│  NMF Topics (latent):                                    │
│  • Topic 1: Data Governance (Art. 10, Art. 25, Art. 28) │
│  • Topic 2: Risk Management (Art. 9, Art. 35)           │
│  • Topic 3: Human Oversight (Art. 14, Art. 27)          │
│  • Topic 4: Transparency (Art. 13, Art. 50)             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Use case — Impact-analyse van een wetswijziging:**
```
Nieuwe richtlijn: "EDPB Guidelines on AI and Data Protection (2026)"
    │
    ▼
NLP Analysis → 12 nieuwe aanbevelingen gedetecteerd
    │
    ▼
Knowledge Graph Query:
  MATCH (new:Recommendation)-[:RELATES_TO]->(existing:Article)
  WHERE existing.wet = "AVG"
  RETURN existing.artikel, new.impact
    │
    ▼
Resultaat:
  • Art. 35 (DPIA): 3 nieuwe criteria voor AI-DPIA's
  • Art. 22 (Geautomatiseerde besluiten): nieuwe uitzonderingen
  • Art. 25 (Privacy by Design): vereist AI-specifieke maatregelen
    │
    ▼
Automatische notificatie naar alle organisaties met AI-verwerkingen
```

**Waarom IT-ers versteld staan:** Dit is geen database — dit is een **redeneermodel**. Je kunt vragen stellen zoals: "Welke verwerkingsactiviteiten worden beïnvloed door deze wetswijziging?" en een exacte lijst krijgen.

**Waarom juridische professionals versteld staan:** De knowledge graph toont **verbanden** tussen wetgeving die niet uit de losse tekst naar voren komen. Bijvoorbeeld: een wijziging in EU AI Act Art. 10 heeft implicaties voor AVG Art. 35 DPIA's — en het systeem detecteert dit automatisch.

### Pijler 4: Continue Compliance-Monitoring

**Het concept:** In plaats van een DPIA éénmaal te schrijven en op te bergen, monitort JuraRegel **continu**:

1. **Document Actualiteit:** Is de DPIA nog actueel? (review-datum)
2. **Evidence Geldigheid:** Is het bewijsstuk nog geldig? (expiry-datum)
3. **Wetswijzigingen:** Is er nieuwe wetgeving die impact heeft?
4. **Implementatie-Drift:** Wijkt de werkelijke implementatie af van de beleidsregel?
5. **Incidenten:** Zijn er incidenten gemeld die de DPIA beïnvloeden?

**Compliance Score Model:**
```
CS = Σ(wᵢ × sᵢ) / Σ(wᵢ)

Criterium                    Weight    Meetmethode
─────────────────────────────────────────────────────
Documentatie Compleetheid     20%      % ingevulde secties
Evidence Actualiteit          15%      % bewijsstukken < 1 jaar
Review-Termijnen              15%      % op tijd herzien
Maatregelen-Implementatie     20%      % geïmplementeerde maatregelen
Incidenten-Afhandeling        10%      % incidenten binnen SLA
Training Actualiteit          10%      % actuele trainingen
Stakeholder-Consultatie       10%      % geraadpleegde stakeholders
```

**Waarom IT-ers versteld staan:** Een compliance-score die **real-time** wordt berekend uit de onderliggende data. Geen Excel-sheet die handmatig wordt bijgehouden, maar een API die de score serveert.

**Waarom juridische professionals versteld staan:** Een objectieve, herhaalbare compliance-score die niet afhankelijk is van de persoon die de audit uitvoert. Dit is wat de AP eist: **demonstreerbare** compliance.

### Pijler 5: Agentic AI Workflows

**Het concept:** AI-agents die compliance-taken **end-to-end** uitvoeren:

| Agent | Taak | Input | Output |
|-------|------|-------|--------|
| **DPIA Agent** | DPIA genereren | Verwerkingsbeschrijving | Volledige DPIA |
| **FRIA Agent** | FRIA genereren | AI-systeem beschrijving | Volledige FRIA |
| **Regulatory Monitor** | Wetswijzigingen monitoren | Bronnen (EUR-Lex, Staatsblad) | Impact-rapport |
| **Evidence Agent** | Evidence verzamelen | Assessment-sectie | Bewijsstukken |
| **Review Agent** | Review-cyclus plannen | Assessment metadata | Review-schema |
| **Incident Agent** | Incident analyseren | Incident-data | Root cause + maatregelen |

**Workflow Voorbeeld — DPIA Agent:**
```
Stap 1: Gebruiker beschrijft verwerking
    │
Stap 2: DPIA Agent voert Pre-scan uit (9 criteria)
    │
Stap 3: Indien GO → Agent genereert volledige DPIA
    │       • Haalt relevante wetgeving op (RAG)
    │       • Genereert risico-analyse per criterium
    │       • Stelt maatregelen voor met juridische basis
    │       • Koppelt evidence-templates
    │
Stap 4: Agent identificeert stakeholders voor consultatie
    │
Stap 5: Agent plant review-cyclus (jaarlijks of bij wijziging)
    │
Stap 6: Agent monitort continu op wetswijzigingen die impact hebben
```

**Waarom IT-ers versteld staan:** Dit is geen chatbot — dit is een **autonoom agent** die een volledige DPIA genereert, stakeholders identificeert, en review-cyclus plant. Met API-integratie voor alle stappen.

**Waarom juridische professionals versteld staan:** De agent genereert niet alleen een document — het genereert een **audit-trail** van elke beslissing, met bron-citaties en confidence-scores. Dit is wat nodig is voor AP-overleg.

---

## 3. Technische Architectuur — Next Leap

### 3.1 Huidige Staat (v3.0)

```
Templates (37) → Render Engine → Markdown/HTML/JSON
Use Cases (50+) → JREM Exports → API Endpoints
Traceability → Wet → Regel → Code → Test → Audit
```

### 3.2 Next Leap (v4.0)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        JURATOOL v4.0                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     AGENT ORCHESTRATOR                          │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │    │
│  │  │ DPIA    │ │ FRIA    │ │Regulatory│ │Evidence │ │ Review  │  │    │
│  │  │ Agent   │ │ Agent   │ │ Monitor  │ │ Agent   │ │ Agent   │  │    │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘  │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     RAG + KNOWLEDGE GRAPH                        │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│  │  │ Hybrid   │  │ Knowledge│  │ Citation │  │ Halluc.  │       │    │
│  │  │ Search   │  │ Graph    │  │ Verify   │  │ Detect   │       │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │    │
│  │                                                                  │    │
│  │  Vector Store: Qdrant    Graph Store: Neo4j/pg_graph            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     COMPLIANCE ENGINE                            │    │
│  │                                                                  │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│  │  │ Score    │  │ Drift    │  │ Policy   │  │ Workflow │       │    │
│  │  │ Engine   │  │ Detect   │  │ as Code  │  │ Engine   │       │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     DATA LAYER                                   │    │
│  │  PostgreSQL + RLS │ Qdrant │ Redis │ Immutable Audit Log       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.3 Data Flow — Van Wet tot Compliance

```
Wetgeving (EUR-Lex, Staatsblad, EDPB)
    │
    ▼
Document Ingestion → Parse → Chunk → Embed → Store (Qdrant)
    │
    ▼
Knowledge Graph Construction (NMF + Manual Curation)
    │
    ▼
Compliance Assessment Generation
    │
    ▼
Continuous Monitoring → Drift Detection → Alert → Remediation
    │
    ▼
Audit Trail → Immutable Log → Export (PDF/JSON)
```

---

## 4. Product Roadmap — Next Leap

### Sprint 1: API Production-Ready (Week 1-2)
- [ ] PostgreSQL schema + migrations
- [ ] Row Level Security (multi-tenant)
- [ ] OAuth2 + API key authentication
- [ ] Rate limiting + throttling
- [ ] API documentation (Swagger UI)

### Sprint 2: RAG Pipeline (Week 3-4)
- [ ] Document ingestion (EUR-Lex, Staatsblad, EDPB)
- [ ] Embedding + vector storage (Qdrant)
- [ ] Hybrid search (BM25 + dense)
- [ ] Re-ranking (cross-encoder)
- [ ] Citation verification

### Sprint 3: Knowledge Graph (Week 5-6)
- [ ] NMF-based topic extraction
- [ ] Graph construction (Neo4j/pg_graph)
- [ ] Relationship inference
- [ ] Impact analysis queries
- [ ] Visualization

### Sprint 4: Agentic Workflows (Week 7-8)
- [ ] DPIA Agent (end-to-end generation)
- [ ] FRIA Agent
- [ ] Regulatory Monitor Agent
- [ ] Evidence Agent
- [ ] Review Scheduler Agent

### Sprint 5: Compliance Dashboard (Week 9-10)
- [ ] Real-time compliance scoring
- [ ] Drift detection alerts
- [ ] Regulatory change feed
- [ ] Audit trail viewer
- [ ] Export (PDF, Excel, JSON)

### Sprint 6: Policy-as-Code (Week 11-12)
- [ ] Rego/OPA policy encoding
- [ ] Automatic validation
- [ ] CI/CD integration
- [ ] Drift detection
- [ ] Compliance gates

---

## 5. Het "Wow" Moment — Demo Scenario

**Scenario:** Een gemeente implementeert een AI-systeem voor WOZ-waardering.

### Stap 1: Registratie (2 minuten)
```
Compliance Officer: "Ik registreer een nieuwe verwerking: WOZ-AI"
JuraRegel:          "Verwerking geregistreerd. Op basis van de 9 EDPB-criteria
                     is een DPIA verplicht (score: 78/100). Een FRIA is niet
                     verplicht (geen hoog-risico AI-systeem volgens Bijlage III).
                     Ik start de DPIA Agent."
```

### Stap 2: DPIA Generatie (5 minuten)
```
DPIA Agent:         "DPIA gegenereerd met 94% confidence.
                     12 risico's geïdentificeerd, 8 maatregelen voorgesteld.
                     Alle beweringen zijn gekoppeld aan bron-citaties.
                     3 secties vereisen menselijke review (confidence < 0.85).
                     Evidence-templates gekoppeld aan elke sectie."
```

### Stap 3: Continue Monitoring (24/7)
```
Regulatory Monitor: "Nieuwe EDPB richtlijn gedetecteerd: 'AI and Data Protection 2026'.
                     Impact op deze verwerking: 3 nieuwe DPIA-criteria van toepassing.
                     Automatische update voorgesteld. Review-cyclus aangepast."
```

### Stap 4: Audit (real-time)
```
Auditor:            "Toon compliance-status voor WOZ-AI."
JuraRegel:          "Compliance Score: 87/100 (Goed).
                     Documentatie: 100% compleet.
                     Evidence: 92% actueel.
                     Review: Volgende review over 8 maanden.
                     Geen openstaande incidenten.
                     Volledige audit-trail beschikbaar."
```

**Dit is het "wow" moment:** Van registratie tot volledige compliance in 5 minuten, met continue monitoring en een compliance-score die real-time wordt berekend.

---

## 6. Conclusie — Waarom Dit een Great Leap Is

| Aspect | Huidige Staat | Next Leap |
|--------|--------------|-----------|
| **Templates** | 37 statische templates | 37 templates + AI-gestuurde invulling |
| **Analyse** | Handmatige interpretatie | RAG-gestuurde juridische reasoning |
| **Monitoring** | Geen | Continue compliance-monitoring |
| **Wetswijzigingen** | Handmatige detectie | Automatische detectie + impact-analyse |
| **Compliance Score** | Niet aanwezig | Real-time score uit onderliggende data |
| **Audit Trail** | Handmatig | Automatisch, immutable |
| **Integratie** | Python-only | REST API + GraphQL + webhooks |
| **Multi-tenancy** | Niet aanwezig | PostgreSQL RLS + OAuth2 |
| **Knowledge** | Geen | Knowledge Graph + NMF |
| **Agents** | Geen | 6 autonome compliance-agents |

**JuraRegel v4.0 is geen incrementele verbetering. Het is de transformatie van een document-generator naar een autonoom compliance-systeem.**

---

*Gegenereerd: 2026-07-20*
*Bronnen: Harvard JOLT (2025), arXiv:2502.20364, SSRN 5162111, Yale LaborBench 2026, GitHub analyse, Centraleyes 2026, Harvey AI, Thomson Reuters*
*Review: FG, AI-verantwoordelijke, CISO, Externe Auditor*
