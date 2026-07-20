# JuraRegel — Diepe Analyse & Uitgebreide Roadmap

**Versie:** 2.0 (2026-07-20)
**Niveau:** PhD — Architectuur · AI/ML · Juridisch · Software Engineering
**Methodologie:** Code Review Graph (1999 nodes, 12365 edges, 21 communities) + OpenMythos + RegTech Research

---

## 0. Executive Summary

JuraRegel heeft een solide basis: 275 bestanden, 37 templates, 40+ API endpoints, 6 AI agents, compliance scoring, en een dashboard. Maar uit de **graph-analyse** (1999 nodes, 75 knowledge gaps) en **RegTech onderzoek** blijkt dat er **5 kritieke blinde vlekken** zijn die het platform nog niet echt "living" maken:

| Blinde Vlek | Impact | Prioriteit |
|-------------|--------|------------|
| **Geen echte RAG** | LLM-output zonder bronnen = hallucinatie-risico | 🔴 Kritiek |
| **Geen drift detection** | Compliance wordt niet continu gemonitord | 🔴 Kritiek |
| **Geen regulatory change detection** | Wetswijzigingen worden niet automatisch gedetecteerd | 🟠 Hoog |
| **Geen Knowledge Graph** | Geen verbanden tussen wetgeving, risico's, maatregelen | 🟠 Hoog |
| **Geen Policy-as-Code integratie** | Policies zijn testbaar maar niet geïntegreerd in CI/CD | 🟡 Middel |

**De next leap:** Van document-generator naar **echte Living Compliance Engine** met RAG-gestuurde analyse, continue monitoring, en automatische wetswijzigingsdetectie.

---

## 1. Codebase Analyse — Graph Intelligence

### 1.1 Architectuur-Overzicht

```
21 Communities gedetecteerd:
├── tests-jrem (757 nodes)       — JREM validatie tests
├── api-list (260 nodes)         — API routes + templates
├── sources-check (139 nodes)    — Bronverificatie
├── templates-template (113)     — Document templates
├── gate-receipt (101)           — Gate + receipt validatie
├── mcp-server-list (63)         — MCP server integratie
├── ci-gate (57)                 — CI/CD gates
├── tools-index (44)             — Tool indexering
├── tests-stap (41)              — Step definitions
├── lib-key (38)                 — Library key functions
├── scripts-validate (27)        — Validatie scripts
├── steps-then (19)              — BDD steps
├── compliance-page (13)         — Compliance dashboard
├── scraper-state (11)           — Scraper state management
├── src-client (10)              — TypeScript SDK
├── scripts-git (8)              — Git scripts
├── bin-safe (8)                 — CLI bin
├── governance-repo (7)          — Governance
├── demo-category (3)            — Demo generator
├── jrem-open-source-validate (3)— JREM validatie
└── openmythos-integration (2)   — OpenMythos evaluatie
```

### 1.2 Knowledge Gaps (75 gevonden)

**50 geïsoleerde nodes** — functies zonder callers:
- `DPIAAgent.__init__`, `FRIAAgent.__init__`, `RegulatoryMonitorAgent.__init__` — agents zijn niet gekoppeld aan orchestrator
- `KeycloakAuth.get_well_known_url`, `require_role` — auth functies onbereikbaar
- `CitationVerifier.verify_citation` — citatie-verificatie niet gekoppeld aan RAG pipeline
- `HallucinationDetector.__init__` — hallucinatie-detector niet gekoppeld

**20 untested hotspots** — hoge-degree nodes zonder testdekking:
- `validate_instance` (degree 51) — kernvalidatie, niet getest
- `render_engine._render_html` (degree 45) — HTML rendering, niet getest
- `scan_codebase` (degree 34) — EU AI Act scanner, niet getest

**Thin communities:**
- `openmythos-integration-evaluate` (2 nodes) — OpenMythos is ondergeïmplementeerd

### 1.3 Kritieke Bevindingen

| Bevinding | Details |
|-----------|---------|
| **Agents zijn geïsoleerd** | DPIA/FRIA/Regulatory agents hebben geen koppeling met de RAG pipeline |
| **RAG is oppervlakkig** | Embedding service gebruikt hash-based fallback, geen echte embeddings |
| **Geen Knowledge Graph** | Geen graph-database voor juridische concept-relaties |
| **Geen drift detection** | Geen continue monitoring van compliance-afwijkingen |
| **OpenMythos is 2 nodes** | Volledig evaluation framework is niet geïntegreerd |

---

## 2. RegTech Marktanalyse — 2026 Trends

### 2.1 Wat marktleiders doen

| Platform | Feature | JuraRegel |
|----------|---------|-----------|
| **Harvey AI** | RAG + legal reasoning | ⚠️ RAG zonder echte embeddings |
| **Thomson Reuters** | Agentic AI workflows | ⚠️ Agents zonder RAG-integratie |
| **OneTrust** | Continuous monitoring | ❌ Geen drift detection |
| **Centraleyes** | Real-time scoring | ✅ Scoring aanwezig |
| **Legora** | Multi-framework | ✅ AVG + AI Act + ISO |

### 2.2 2026 RegTech Trends (volgens Stanford, Deloitte, RegPulse)

1. **AI-gestuurde compliance monitoring** — 70% compliance officers tillen naar automated monitoring
2. **Agentic AI** — autonome agents die taken end-to-end uitvoeren
3. **RAG + Knowledge Graphs** — combinatie van retrieval en reasoning
4. **Drift detection** — continue monitoring van implementatie vs. beleid
5. **Regulatory change automation** — automatische detectie + impact-analyse
6. **Compliance-as-Code** — policies als testbare, versioneerbare code

---

## 3. De 5 Blinde Vlekken — Analyse & Mitigatie

### Blinde Vlek 1: Geen echte RAG (Kritiek)

**Huidige staat:** De RAG pipeline gebruikt hash-based fallback embeddings. De vector store is in-memory en verliest data bij herstart. Er is geen echte LLM-integratie voor juridische reasoning.

**Mitigatie — Echte RAG Pipeline:**
```python
# Huidig: hash-based fallback
embedding = self._fallback_embed(text)  # 384-dim hash

# Toekomst: echte embeddings via Qdrant + sentence-transformers
embedding = self.embedder.embed(text)  # all-MiniLM-L6-v2 of text-embedding-3-large

# + LLM-integratie via LiteLLM
response = llm.generate(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "system", "content": LEGAL_SYSTEM_PROMPT},
              {"role": "user", "content": query}],
    context=retrieved_chunks
)
```

**Implementatie:**
1. Qdrant collection aanmaken met juiste distance metric (COSINE)
2. Sentence-transformers model laden (all-MiniLM-L6-v2, lokaal)
3. Document ingestion pipeline (EUR-Lex scraper → chunking → embedding → Qdrant)
4. LLM-integratie via LiteLLM proxy (werkstation:192.168.1.28:4000)
5. Citation verification + hallucination detection

### Blinde Vlek 2: Geen drift detection (Kritiek)

**Huidige staat:** Compliance score wordt éénmaal berekend, niet continue gemonitord.

**Mitigatie — Drift Detection Engine:**
```python
class DriftDetector:
    """Continue monitoring van compliance-afwijkingen."""

    def detect_drift(self, assessment_id: str) -> DriftReport:
        baseline = self.get_baseline(assessment_id)
        current = self.get_current_state(assessment_id)

        drift = []
        # 1. Beleid vs. Implementatie
        for measure in baseline.measures:
            if measure.status != current.get(measure.id):
                drift.append(DriftItem(
                    type="implementation",
                    measure=measure.name,
                    expected=measure.status,
                    actual=current.get(measure.id),
                    severity="high"
                ))

        # 2. Wetswijzigingen
        changes = self.regulatory_monitor.get_changes_since(baseline.last_review)
        for change in changes:
            if change.affects(assessment_id):
                drift.append(DriftItem(
                    type="regulatory",
                    change=change.title,
                    impact=change.impact_score,
                    severity="critical"
                ))

        # 3. Evidence geldigheid
        for evidence in baseline.evidence:
            if evidence.is_expired():
                drift.append(DriftItem(
                    type="evidence_expired",
                    evidence=evidence.title,
                    severity="medium"
                ))

        return DriftReport(drift=drift, score=self.calculate_drift_score(drift))
```

### Blinde Vlek 3: Geen regulatory change detection (Hoog)

**Huidige staat:** De Regulatory Monitor Agent returned hardcoded data.

**Mitigatie — Echte Regulatory Monitor:**
```python
class RegulatoryMonitor:
    """Automatische detectie van wetswijzigingen."""

    SOURCES = [
        ("EUR-Lex", "https://eur-lex.europa.eu/api/search"),
        ("Staatsblad", "https://www.officielebekendmakingen.nl/api"),
        ("EDPB", "https://edpb.europa.eu/news/news_en"),
        ("AP", "https://www.autoriteitpersoonsgegevens.nl/nl/nieuws"),
    ]

    async def scan(self) -> list[RegulatoryChange]:
        changes = []
        for source, url in self.SOURCES:
            latest = await self.scraper.scrape(url)
            previous = self.store.get_latest(source)
            diff = self.diff(previous, latest)
            if diff.has_changes:
                changes.append(RegulatoryChange(
                    source=source,
                    title=diff.title,
                    summary=diff.summary,
                    impact_score=self.analyze_impact(diff),
                    affected_frameworks=self.identify_frameworks(diff)
                ))
        return changes
```

### Blinde Vlek 4: Geen Knowledge Graph (Hoog)

**Huidige staat:** Geen graph-database voor juridische concept-relaties.

**Mitigatie — Juridische Knowledge Graph:**
```python
# Neo4j/pg_graph schema
NODES = ["Wet", "Artikel", "Richtlijn", "Uitspraak", "Template", "Criterion", "Risico", "Maatregel"]
EDGES = ["has_article", "references", "requires", "contradicts", "supersedes", "implements", "has_criterion"]

# Cypher query voor impact-analyse
"""
MATCH (change:Artikel {wet: "EU AI Act"})-[:requires]->(template:Template)
      -[:has_criterion]->(criterion:Criterion)
MATCH (criterion)<-[:has_criterion]-(existing:Assessment)
RETURN existing.id, criterion.name, change.impact_score
"""
```

### Blinde Vlek 5: OpenMythos ondergeïmplementeerd (Middel)

**Huidige staat:** OpenMythos integratie bestaat uit 2 nodes (evaluator).

**Mitigatie — Volledige OpenMythos Integratie:**
- Uitbreiden CATEGORY_MAP naar alle 10 OpenMythos categorieën
- Koppelen aan code-scanner voor EU AI Act compliance
- Genereren van benchmark reports
- Integreren met CI/CD gates

---

## 4. Uitgebreide Roadmap — Next Leap

### Sprint 7: Echte RAG Pipeline (Week 1-2)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 7.1 | Qdrant setup | Collection + indexing | Recall@k benchmark |
| 7.2 | Sentence-transformers | all-MiniLM-L6-v2 lokaal | Embedding quality test |
| 7.3 | Document ingestion | EUR-Lex + Staatsblad scraper | 100+ documenten geïndexeerd |
| 7.4 | LLM-integratie | LiteLLM proxy connectie | Claude-sonnet-4 response |
| 7.5 | Citation verification | Bron-check per claim | <5% hallucinatie-rate |

### Sprint 8: Drift Detection (Week 2-3)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 8.1 | Baseline versioning | Assessment snapshots | Version diff |
| 8.2 | Implementation monitoring | Maatregel-tracking | Drift alerts |
| 8.3 | Evidence expiry | Automatische notificatie | Expiry alerts |
| 8.4 | Compliance trending | Score over tijd | Trend grafiek |

### Sprint 9: Regulatory Monitor (Week 3-4)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 9.1 | EUR-Lex scraper | Dagelijkse scan | Change detection |
| 9.2 | Staatsblad scraper | Dagelijkse scan | Change detection |
| 9.3 | Impact analyzer | Automatische impact-score | Accuracy test |
| 9.4 | Notification service | E-mail + webhook | Delivery test |

### Sprint 10: Knowledge Graph (Week 4-5)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 10.1 | Neo4j/pg_graph setup | Graph database | Schema validatie |
| 10.2 | Graph construction | Nodes + edges uit corpus | Coverage test |
| 10.3 | Impact queries | Cypher queries voor impact | Query correctness |
| 10.4 | Visualisatie | Graph UI in dashboard | Usability test |

### Sprint 11: OpenMythos Volledig (Week 5-6)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 11.1 | Uitgebreide CATEGORY_MAP | 10 categorieën | Coverage |
| 11.2 | Code scanner integratie | EU AI Act checks | Accuracy |
| 11.3 | Benchmark generation | Rapport per categorie | Compleetheid |
| 11.4 | CI/CD integratie | Gate in workflow | Pass/fail |

### Sprint 12: Policy-as-Code CI/CD (Week 6-7)

| # | Component | Deliverable | Validatie |
|---|-----------|-------------|-----------|
| 12.1 | Rego policies | OPA-compatible rules | Policy tests |
| 12.2 | CI integration | GitHub Actions gate | Build pass/fail |
| 12.3 | Drift alerts | Automatische notificatie | Alert delivery |
| 12.4 | Compliance dashboard | Real-time score + trend | Live data |

---

## 5. Architectuur — Toekomstige Staat

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        JURATOOL v5.0                                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                     AGENT ORCHESTRATOR                          │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │    │
│  │  │ DPIA    │ │ FRIA    │ │Regulatory│ │ Drift   │ │ Policy  │  │    │
│  │  │ Agent   │ │ Agent   │ │ Monitor  │ │ Detector│ │ Agent   │  │    │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘  │    │
│  │       └────────────┴────────────┴────────────┴────────────┘     │    │
│  │                                    │                             │    │
│  │                          ┌─────────┴─────────┐                   │    │
│  │                          │   RAG PIPELINE     │                   │    │
│  │                          │  ┌──────────────┐  │                   │    │
│  │                          │  │ LLM (Claude) │  │                   │    │
│  │                          │  │ via LiteLLM  │  │                   │    │
│  │                          │  └──────────────┘  │                   │    │
│  │                          └───────────────────┘                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                   KNOWLEDGE GRAPH                                │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │    │
│  │  │ Wetten   │  │ Artikelen│  │ Risico's │  │Maatregelen│       │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │    │
│  │  Edges: has_article, references, requires, contradicts          │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                    │                                     │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                      DATA LAYER                                  │    │
│  │  PostgreSQL + RLS │ Qdrant │ Neo4j │ Redis │ Immutable Audit   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Conclusie — De Next Leap

JuraRegel heeft een unieke positie: **de enige open-source compliance engine die vertrekt van juridische regels en deze vertaalt naar IT-uitvoering.** Maar om echt een "Living Compliance Engine" te worden, moet het platform 5 kritieke uitbreidingen krijgen:

| Uitbreiding | Impact | Complexiteit |
|-------------|--------|--------------|
| Echte RAG (Qdrant + LLM) | 🔴 Kritiek | Hoog |
| Drift Detection | 🔴 Kritiek | Middel |
| Regulatory Monitor | 🟠 Hoog | Hoog |
| Knowledge Graph | 🟠 Hoog | Hoog |
| OpenMythos Volledig | 🟡 Middel | Middel |

**Totale geschatte inspanning:** 7 weken (1 sprint per 1-2 weken)

**Het resultaat:** Een platform dat niet alleen documenten genereert, maar **continue compliance garandeert** — van wetgeving tot implementatie, van detectie tot remediatie.

---

*Gegenereerd: 2026-07-20*
*Methodologie: Code Review Graph (1999 nodes, 12365 edges, 21 communities, 75 gaps) + OpenMythos + RegTech Marktanalyse*
*Volgende sprint: Sprint 7 — Echte RAG Pipeline*
