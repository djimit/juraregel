# JuraRegel — Legal RuleOps Platform

[![JuraRegel CI](https://github.com/djimit/juraregel/actions/workflows/juraregel-ci.yml/badge.svg)](https://github.com/djimit/juraregel/actions/workflows/juraregel-ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Use Cases](https://img.shields.io/badge/Use%20Cases-28-blue)](https://github.com/djimit/juraregel)
[![Tests](https://img.shields.io/badge/Tests-451%2B-green)](https://github.com/djimit/juraregel)
[![Regels](https://img.shields.io/badge/JREM%20Regels-655-purple)](https://github.com/djimit/juraregel)
[![Agentic](https://img.shields.io/badge/Agentic-Platform-orange)](https://github.com/djimit/juraregel)
[![MCP](https://img.shields.io/badge/MCP-12%20tools%20%2B%203%20resources%20%2B%203%20prompts-teal)](https://github.com/djimit/juraregel)
[![BDD](https://img.shields.io/badge/BDD-7%20scenarios-brightgreen)](https://github.com/djimit/juraregel)
[![Schema](https://img.shields.io/badge/JREM-Schema%20v1.1.0-lightblue)](https://github.com/djimit/juraregel)

> **Juridische regels die juristen schrijven en computers begrijpen.**
>
> **[🎮 Probeer de Playground](https://djimit.github.io/juraregel/)** — compliance checking in je browser, geen installatie nodig.

JuraRegel is een open-source platform voor het beheren, valideren, versioneren en serveren van administratief-juridische regels. Het vertaalt bijvoorbeeld de [pseudonimiseringsrichtlijn](https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn) van Rechtspraak.nl en andere juridische richtlijnen naar digitale, testbare, auditeerbare regels.

> **Disclaimer:** JuraRegel is een proof-of-concept en architectuurprototype. Het is niet geschikt voor productiegebruik als juridisch besluitvormingsplatform zonder onafhankelijke juridische validatie.

## Wat JuraRegel doet

- **Pseudonimiseringsrichtlijn Engine** — classificeert persoonsgegevens in uitspraken conform de richtlijn (particulier → pseudonimiseer, professional/organisatie/overheid → niet pseudonimiseer)
- **JREM** — Judicial Rule Exchange Model, versioned JSON Schema standaard (v1.0.0 → v1.1.0) voor juridische regels
- **Rule APIs** — stateless, idempotente APIs met uitleg, bronverwijzingen en audit trail
- **MCP Server** — 12 tools + 3 resources + 3 prompts voor LLM-agents (Claude, GPT, lokale LLMs)
- **Knowledge Base** — 655 regels semantisch doorzoekbaar (Qdrant vector store + SQLite FTS5)
- **BDD Tests** — Gherkin scenarios voor legal team acceptatie (pytest-bdd)
- **BWB Harvester** — automatische wetwijziging-detectie via BWB API
- **CI/CD Gates** — 18+ gates: per-use-case (14), JKB (5), extraction (3), schema versioning, BDD, harvester health
- **RegelSpraak** — Controlled Natural Language specificaties, leesbaar door juristen

## Pseudonimiseringsrichtlijn Engine

De engine (V4.2) classificeert gedetecteerde persoonsgegevens in rechterlijke uitspraken:

| Classificatie | Actie | Voorbeeld |
|---|---|---|
| Particulier | Pseudonimiseer | Geboortedatum van eiser → `[geboortedatum]` |
| Professional | Niet pseudonimiseren | Geboortedatum van advocaat → laten staan |
| Rechtspersoon | Niet pseudonimiseren | Adres van B.V. → laten staan |
| Overheid | Niet pseudonimiseren | Adres van gemeente → laten staan |

**Nauwkeurigheid**: Gevalideerd op dataset van 25.127 uitspraken (48.702 detecties). Geen onafhankelijke gouden standaardvalidatie — resultaten zijn indicatief, niet juridisch bindend.

De engine implementeert de uitzonderingen uit de pseudonimiseringsrichtlijn:
- Professionals bij de procedure (advocaten, notarissen, deurwaarders) → niet pseudonimiseren
- Personen handelend in professionele functie → niet pseudonimiseren
- Rechtspersonen en overheidsorganisaties → niet pseudonimiseren
- Per rechtsgebied verschillende regels (familierecht = strenger, strafrecht = strenger voor particulieren)

## Waarom JuraRegel?

| Aspect | Handmatige compliance check | Commerciële GRC tools | **JuraRegel** |
|---|---|---|---|
| Prijs | €0 (maar uren werk) | €10K-€100K/jaar | **€0 (open-source)** |
| Bronverwijzing per regel | Handmatig | Soms | **Altijd (JREM sourceRef)** |
| Testbaarheid | Geen | Beperkt | **207 tests + 14 CI gates** |
| Uitleg aan burgers | Niet mogelijk | Niet mogelijk | **Redeneerstappen + bronverwijzing** |
| Versiebeheer | Excel/version control | Vendor-locked | **Git + JREM versioning** |
| Developer SDK | Niet beschikbaar | Vendor-locked | **TypeScript SDK (MIT)** |
| Zelf hosten | n.v.t. | Cloud-only | **Docker compose (localhost)** |
| Rule Maturity Model | Niet | Niet | **L1-L4 classificatie** |
| NORA compliance | Niet | Soms | **NORA matrix (15 principes)** |
| Pseudonimisering | Handmatig | Niet | **V4.2 engine (hoog op 25K)** |

## Use Case: Griffierecht

**Als** griffier **wil ik** bij zaakintake automatisch het correcte griffierecht bepalen **zodat** ik niet handmatig tarieven hoeft op te zoeken en fouten voorkom.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Verschillende tarieven per zaakstroom, partijtype en vorderingwaarde — foutgevoelig | Rule API berekent bedrag met bronverwijzing en redeneerstappen |
| Burger | Begrijpt niet waarom een bepaald bedrag geldt | API retourneert uitleg: "vordering €125.000 → categorie >€100K-≤€1M → tarief 2026: €2.803. Bron: Wgbz art. 2" |
| Advocaten | Moeten griffie bellen voor tariefbevestiging | Directe berekening via API of portaal |
| Financieel beheer | Geen audit trail van griffierecht-berekeningen | Elke berekening heeft inputHash, rulesetHash, timestamp |

- 18 JREM regels voor civiele dagvaardingszaken (kanton + handel)
- 57 tests — 14 CI gates — Rule API op `localhost:8490`
- Juridische context in elke response (wet, BWBR-id, accordering)

### Voorbeeld

```bash
curl -X POST http://127.0.0.1:8490/v1/griffierecht/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "calculationDate": "2026-07-03",
    "zaak": {
      "rechtsgebied": "civiel",
      "zaakstroom": "handel",
      "procedureType": "dagvaarding",
      "vorderingWaarde": 125000,
      "bijzondereCategorie": "geen"
    },
    "partij": {
      "rol": "eiser",
      "partijType": "natuurlijk_persoon",
      "onvermogend": false,
      "verweerStatus": "n.v.t."
    }
  }'
```

## Use Case: BIO2 — Baseline Informatiebeveiliging Overheid

**Als** CISO van een overheidsorganisatie **wil ik** automatisch valideren of mijn organisatie voldoet aan de BIO2 maatregelen **zodat** ik niet handmatig 167 maatregelen hoef te checken en ENSIA-rapportage foutloos is.

| Rol | Probleem | Oplossing |
|---|---|---|
| CISO | 167 BIO2 maatregelen handmatig bijhouden in spreadsheet — foutgevoelig en verouderd | Rule API checkt per maatregel: compliant ja/nee + ISO referentie |
| Bestuurder | Onduidelijk welke maatregelen nog open staan | Compliance rapport: per categorie score + totaal % compliant |
| CIP | Geen gestandaardiseerd controle-instrument voor alle entiteiten | JuraRegel als open-source compliance tool — één standaard |
| ENSIA-verantwoordelijke | Handmatige rapportage is tijdrovend en inconsistent | `GET /v1/bio2/rapport/{orgId}` genereert ENSIA-gealigned rapport |
| Auditor | Geen audit trail van compliance-beslissingen | Elke check heeft calculationId, inputHash, rulesetHash, timestamp |

De [BIO2](https://www.bio-overheid.nl/category/producten/bio) is het normenkader voor informatiebeveiliging binnen alle overheidsentiteiten, gebaseerd op ISO 27001/27002. De 167 maatregelen staan op [GitHub (MinBZK)](https://github.com/MinBZK/Baseline-Informatiebeveiliging-Overheid).

- **162 overheidsmaatregelen** geparsed van MinBZK GitHub (5 zijn ISO-only)
- 4 categorieën: organisatorisch (72), technologisch (66), fysiek (17), mensgericht (12)
- Elke maatregel gekoppeld aan ISO 27002 clause (bronverwijzing)
- Rule API op `localhost:8494` — ENSIA-gealigned compliance rapport
- 18 tests — 14 CI gates

### Voorbeeld

```bash
# Lijst alle maatregelen
curl http://127.0.0.1:8494/v1/bio2/maatregelen

# Compliance rapport per organisatie
curl http://127.0.0.1:8494/v1/bio2/rapport/gemeente-amsterdam
```

## Use Case: Forum Standaardisatie — Verplichte Open Standaarden

**Als** architect van een overheidsorganisatie **wil ik** automatisch valideren of mijn organisatie de verplichte open standaarden toepast **zodat** ik niet handmatig de Forum Standaardisatie lijst hoef te checken en Monitor-rapportage foutloos is.

| Rol | Probleem | Oplossing |
|---|---|---|
| Architect | 22 standaarden handmatig bijhouden — verouderd | Rule API checkt per standaard: compliant ja/nee |
| CIO | Onduidelijk welke verplichte standaarden ontbreken | Compliance rapport per categorie |
| Forum Standaardisatie | Geen gestandaardiseerd controle-instrument | JuraRegel als open-source compliance tool |
| Monitor-verantwoordelijke | Handmatige rapportage inconsistent | `GET /v1/fs/rapport/{orgId}` — Monitor aligned |

De [Forum Standaardisatie](https://www.forumstandaardisatie.nl/open-standaarden/verplicht) beheert de lijst van verplichte open standaarden voor de hele Nederlandse overheid — van OAuth en SAML tot DKIM en PDF.

- **22 standaarden** (16 verplicht + 6 streefbeeld) in 4 categorieën
- Interoperabiliteit (OAuth, SAML, OData, StUF, ebMS), Veiligheid (DKIM, DMARC, SPF, TLS, DNSSEC), Document (PDF, OOXML, ODF, eFactuur), Identiteit (eIDAS, iGOV)
- Rule API op `localhost:8495` met standaarden listing en Monitor aligned rapport
- 15 tests — 14 CI gates

### Voorbeeld

```bash
# Lijst alle verplichte standaarden
curl http://127.0.0.1:8495/v1/fs/standaarden?status=verplicht

# Monitor Open Standaarden rapport
curl http://127.0.0.1:8495/v1/fs/rapport/ministerie-bzk
```

## Use Case: Overheidsstandaarden — API, Authenticatie en Events

**Als** API architect bij een overheidsorganisatie **wil ik** automatisch valideren of mijn APIs en services voldoen aan de Logius en Forum Standaardisatie standaarden **zodat** ik niet handmatig regels hoef te checken en developer.overheid.nl registratie foutloos is.

| Rol | Probleem | Oplossing |
|---|---|---|
| API architect | API Design Rules handmatig per endpoint | Rule API checkt per regel: compliant ja/nee |
| Security engineer | OAuth/OIDC profiel incompleet | Check NL GOV Assurance Profile OAuth 2.0 |
| Event architect | CloudEvents niet conforme | Check NL GOV Profile for CloudEvents |
| Integratie architect | Digikoppeling protocol onduidelijk | Check WUS/ebMS/certificaat regels |

24 standaarden uit [Logius](https://logius-standaarden.github.io/API-Design-Rules/), [Forum Standaardisatie](https://www.forumstandaardisatie.nl/open-standaarden/authenticatie-standaarden) en [developer.overheid.nl](https://developer.overheid.nl/):

- **API Design** (14): RESTful, HAL, JSON, camelCase, self-link, error responses, versioning, pagination, CORS, HTTPS
- **Authenticatie** (4): OAuth 2.0 NL GOV Assurance Profile, eIDAS SAML, OpenID Connect, JWT
- **Events** (3): CloudEvents structured mode, extensies
- **Digikoppeling** (3): WUS 3.0, ebMS 3.0, PKIoverheid certificaten
- Rule API op `localhost:8496` — 16 tests — 14 CI gates

### Voorbeeld

```bash
# Lijst alle API Design Rules
curl http://127.0.0.1:8496/v1/os/standaarden?categorie=api-design

# Compliance rapport
curl http://127.0.0.1:8496/v1/os/rapport/ministerie-bzk
```

## Use Case: NORA — Architectuur Compliance (Meta-laag)

**Als** enterprise architect bij een overheidsorganisatie **wil ik** automatisch valideren of mijn oplossing voldoet aan NORA principes **zodat** ik NORA compliance kan bewijzen met verwijzingen naar specifieke use cases.

| Rol | Probleem | Oplossing |
|---|---|---|
| Enterprise architect | NORA compliance handmatig per principe | Rule API checkt 15 NORA principes |
| CIO | Onduidelijk welke principes open staan | NORA compliance matrix met use case mapping |
| TOGAF architect | Principes niet gekoppeld aan implementatie | Matrix mapped principes → JuraRegel use cases |

NORA is de **overkoepelende architectuurlaag** die alle use cases verbindt. 15 principes in 5 categorieën (architectuur, serviceorientatie, beveiliging, identiteit, data). Rule API op `localhost:8497` met `GET /v1/nora/matrix` voor compliance matrix.

## Use Case: EU AI Act — AI-systeem Compliance

**Als** AI-developer **wil ik** automatisch valideren of mijn AI-systeem voldoet aan de EU AI Act **zodat** ik niet handmatig 12 artikelen hoef te checken.

| Rol | Probleem | Oplossing |
|---|---|---|
| AI developer | Onbekend welke verplichtingen van toepassing zijn | Rule API classificeert: verboden/hoog/beperkt/minimaal |
| Compliance officer | Conformity assessment onduidelijk | Check art. 9-12 + 43 |

12 regels (classificatie, conformity, transparantie, rechten). Rule API op `localhost:8498`. Bron: EUR-Lex.

## Use Case: AVG/GDPR — Privacy Compliance

**Als** privacy officer of FG **wil ik** automatisch valideren of mijn organisatie voldoet aan de AVG **zodat** ik niet handmatig 10 artikelen hoef te checken.

| Rol | Probleem | Oplossing |
|---|---|---|
| Privacy officer | DPIA vereisten onduidelijk | Check art. 35 |
| FG | Bewaartermijnen niet systematisch | Check art. 5 lid 1e |
| Web developer | Rechten van betrokkenen onbekend | Check art. 12-22 |

10 regels (DPIA, bewaartermijn, rechten, minimisation). Rule API op `localhost:8499`. Bron: wetten.overheid.nl (UAVG).

## Use Case: NCSC — ICT-beveiligingsrichtlijnen

**Als** security engineer **wil ik** automatisch valideren of mijn systemen voldoen aan de NCSC ICT-beveiligingsrichtlijnen **zodat** ik niet handmatig 32 richtlijnen hoef te checken.

| Rol | Probleem | Oplossing |
|---|---|---|
| Security engineer | 32 NCSC richtlijnen handmatig | Rule API checkt per richtlijn: compliant ja/nee |
| CISO | Onbekend wat open staat | Compliance rapport per categorie (TLS, webapp, basisprincipes) |
| Web developer | Webapp richtlijnen onduidelijk | Check input validatie, output encoding, CSRF, CSP |
| SRE-er | TLS richtlijnen niet systematisch | Check TLS 1.2+, cipher suites, HSTS, cert pinning |

32 richtlijnen uit [NCSC](https://www.ncsc.nl/basisprincipes): TLS (8), Webapplicaties (10), Basisprincipes (14). Rule API op `localhost:8500`.

### Voorbeeld

```bash
# Lijst alle TLS richtlijnen
curl http://127.0.0.1:8500/v1/ncsc/richtlijnen?categorie=tls

# Compliance rapport
curl http://127.0.0.1:8500/v1/ncsc/rapport/gemeente-amsterdam
```

## Product Features

### Docker Compose
```bash
docker compose up  # Start alle 8 Rule APIs
```

### CLI: Nieuwe Use Case Scaffolden
```bash
bash juraregel-init.sh avg 8498  # Scaffold een AVG use case op port 8498
```

### GitHub Actions CI
```yaml
# In je eigen repo:
jobs:
  juraregel:
    uses: djimit/juraregel/.github/workflows/juraregel-ci.yml@main
    with:
      use-case: 'all'
```

### Dashboard
Open `dashboard/index.html` voor een visueel overzicht van alle 10 use cases met poorten, regels en status.

### Contributing
Zie [CONTRIBUTING.md](CONTRIBUTING.md) voor de use case template en bijdrage richtlijnen.

### NORA Compliance Matrix
Zie [docs/nora-compliance-matrix.md](docs/nora-compliance-matrix.md) voor de Mermaid diagram met NORA principes → use case mapping.

## Voor elk rol in het functiehuis Rijksoverheid

| Rol | Wat JuraRegel biedt | Start hier |
|---|---|---|
| AI Engineer | EU AI Act compliance (12 regels) | [EU AI Act use case](docs/eu-ai-act-use-case.md) |
| Data Engineer | AVG data minimisation, bewaartermijnen | [AVG use case](docs/avg-gdpr-use-case.md) |
| Software Ontwikkelaar | TypeScript SDK, CLI, OpenAPI, code examples | [SDK README](sdk/typescript/README.md), [examples](docs/examples/) |
| Solution Architect | NORA matrix, API Design Rules, ADR template | [NORA use case](docs/nora-use-case.md), [ADR template](docs/templates/adr-template.md) |
| Security Expert | BIO2 (162), NCSC (32), threat model template | [BIO2](docs/bio2-use-case.md), [NCSC](docs/ncsc-use-case.md), [threat model](docs/templates/threat-model-template.md) |
| DevOps Engineer | Docker compose, Helm chart, GitHub Actions | [Docker](#docker), [Helm](helm/), [CI](.github/workflows/) |
| SRE | Health endpoints, Grafana dashboard, runbook | [Grafana](docs/sre/grafana-dashboard.json), [runbook](docs/sre/runbook-template.md) |
| Tester | 451+ tests (unit + BDD + MCP), test templates | [CONTRIBUTING](CONTRIBUTING.md), [user story template](docs/templates/user-story-template.md) |
| Product Owner | Compliance rapporten, ROI template, comparison | [Comparison table](#waarom-juraregel), [user story template](docs/templates/user-story-template.md) |
| Enterprise Architect | NORA compliance matrix, TOGAF mapping, C4 | [NORA matrix](docs/nora-compliance-matrix.md), [ADR template](docs/templates/adr-template.md) |
| Compliance Officer | Multi-framework compliance, ENSIA rapport | [Executive dashboard](dashboard/executive.html), [Postman](docs/juraregel-postman-collection.json) |
| CISO | BIO2 + NCSC + Cybersecuritybeeld 2025 | [Executive dashboard](dashboard/executive.html), [NCSC](docs/ncsc-use-case.md) |
| Jurist | RegelSpraak CNL, bronverwijzingen, acceptatie | [Rule Extraction Sprint](docs/rule-extraction-sprint.md), [maturity model](docs/maturity-model.md) |
| Privacy Officer | AVG/GDPR regels, DPIA template | [AVG use case](docs/avg-gdpr-use-case.md), [DPIA template](docs/templates/dpia-template.md) |
| Beleidsmedewerker | NORA principes, Forum Standaardisatie | [NORA](docs/nora-use-case.md), [Forum Standaardisatie](docs/forumstandaardisatie-use-case.md) |

### Templates & Tooling

| Wat | Waar | Voor wie |
|---|---|---|
| ADR template | [docs/templates/adr-template.md](docs/templates/adr-template.md) | Architecten |
| Threat model template | [docs/templates/threat-model-template.md](docs/templates/threat-model-template.md) | Security experts |
| DPIA template | [docs/templates/dpia-template.md](docs/templates/dpia-template.md) | Privacy officers |
| User story template | [docs/templates/user-story-template.md](docs/templates/user-story-template.md) | Product owners |
| Grafana dashboard | [docs/sre/grafana-dashboard.json](docs/sre/grafana-dashboard.json) | SRE |
| Runbook template | [docs/sre/runbook-template.md](docs/sre/runbook-template.md) | SRE |
| Postman collection | [docs/juraregel-postman-collection.json](docs/juraregel-postman-collection.json) | Ontwikkelaars |
| Code examples | [docs/examples/](docs/examples/) — Python, Java, C#, Go, TypeScript | Ontwikkelaars |
| Executive dashboard | [dashboard/executive.html](dashboard/executive.html) | C-level |
| Compliance matrix | [shared/compliance_matrix.py](shared/compliance_matrix.py) | Compliance officers |
| Helm chart | [helm/juraregel/](helm/juraregel/) | DevOps |

## Installatie

### TypeScript SDK
```bash
npm install @juraregel/sdk
```

### CLI
```bash
npx juraregel init avg 8500    # Scaffold nieuwe use case
npx juraregel check             # Run CI gates
npx juraregel serve griffierecht # Start API
npx juraregel validate use-cases/griffierecht/jrem/exports/griffierecht-civiel-2026.1.json
```

### Docker
```bash
docker compose up  # Start alle 10 Rule APIs (ports 8490-8499)
```

### Dashboard
Open `dashboard/index.html` voor een visueel overzicht met live health checks.

## Architectuur

```mermaid
graph TB
    subgraph "Bronnen"
        R[Rechtspraak.nl]
        B[MinBZK GitHub — BIO2]
        F[Forum Standaardisatie]
        L[Logius / developer.overheid.nl]
        N[noraonline.nl]
        EU[EUR-Lex — EU AI Act]
        AVG[wetten.overheid.nl — AVG]
    end

    subgraph "JuraRegel Platform"
        RS[RegelSpraak CNL]
        JREM[JREM JSON Schema 2020-12]
        CI[CI/CD — 14 Gates]
        API[Rule API — FastAPI :8490-8499]
    end

    subgraph "Consumers"
        SDK[TypeScript SDK — @juraregel/sdk]
        CLI[npx juraregel]
        DASH[Dashboard]
        PLAY[Playground]
        DOCKER[docker compose up]
        GH[GitHub Actions]
    end

    R --> RS
    B --> RS
    F --> RS
    L --> RS
    N --> RS
    EU --> RS
    AVG --> RS
    RS --> JREM
    JREM --> CI
    CI --> API
    API --> SDK
    API --> CLI
    API --> DASH
    API --> PLAY
    API --> DOCKER
    CI --> GH
```

### Use Case Maturity

| Use case | Regels | Status | Poort |
|---|---|---|---|
| Griffierecht | 36 | **PoC** | 8490 |
| BIO2 | 162 | **PoC** | 8494 |
| Forum Standaardisatie | 22 | **PoC** | 8495 |
| Overheidsstandaarden | 24 | **PoC** | 8496 |
| NORA | 15 | **PoC** | 8497 |
| EU AI Act | 12 | PoC | 8498 |
| EU AI Act | 12 | PoC | 8498 |
| AVG/GDPR | 10 | PoC | 8499 |
| **NCSC** | **32** | **Production** | **8500** |
| Procesreglement | 4 | PoC | 8491 |
| Classificatie | 3 | PoC | 8492 |
| Publicatie/PII | 3 | **Production** (engine V4.2) | 8493 |

├── griffierecht/         Eerste use case (bewezen PoC)
├── procesreglement/      UC-02: Digitale indiening
├── classificatie/        UC-03: Zaakclassificatie
└── publicatie/           UC-06: Pseudonimiseringsrichtlijn engine
shared/
├── api_base.py           Factory pattern: create_app(domain, jrem_path, port)
├── jrem-schema.json      JSON Schema 2020-12 (open standaard)
├── validate.py           JREM validator
└── registry.py           Multi-domein index
ci/
├── run-gates.sh          14 CI gates per use case
├── run-all-gates.sh      CI driver voor alle use cases
└── acceptatie-check.py   Gate 14: jurist-acceptatie
```

## Pseudonimiseringsrichtlijn Engine bestanden

| Bestand | Beschrijving |
|---|---|
| `use-cases/publicatie/lib/richtlijn_engine.py` | V1: Basis classificatie (95% target) |
| `use-cases/publicatie/lib/richtlijn_engine_v2.py` | V2: Sentence-level + confidence scoring (99% target) |
| `use-cases/publicatie/lib/richtlijn_engine_v3.py` | V3: Scanner-level fixes (99.995% target) |
| `use-cases/publicatie/lib/richtlijn_engine_v4.py` | V4.2: Final — `\bOM\b` fix, particulier confirm, woont-aan override (hoog op 25K) |
| `use-cases/publicatie/regelspraak/pseudonimiseringsrichtlijn.rspraak` | 17 RegelSpraak regels conform richtlijn |
| `use-cases/publicatie/tests/test_richtlijn_engine.py` | 16 tests voor de engine |

## Installatie

```bash
git clone https://github.com/djimit/juraregel.git
cd juraregel
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic jsonschema pytest httpx

# Run tests
python3 -m pytest use-cases/*/tests/ -v

# Start griffierecht API
python3 use-cases/griffierecht/api/app.py
# → http://127.0.0.1:8490/v1/health

# Open demo
open demo/index.html

# Run CI gates
bash ci/run-all-gates.sh
```

## JREM Open Standaard

JREM (Judicial Rule Exchange Model) is een open JSON Schema (draft 2020-12) voor het structureren van juridische regels:

- Regels met voorwaarden, uitkomsten en bronverwijzingen
- Ingebedde test scenario's
- Versiebeheer met geldigheidsperiodes
- Metadata met juridische context en jurist-acceptatie

Zie `jrem-open-source/` voor het standalone JREM schema, validator en examples.

## Validatie

| Metriek | Waarde |
|---|---|
| Use cases | 4 (griffierecht, procesreglement, classificatie, publicatie) |
| Tests | 224 (alle groen) |
| CI gates | 14 per use case |
| JREM regels | 46 |
| Pseudonimisering engine | V4.2 — hoog op 25.127 uitspraken |
| Open standaarden | 7 compliant (pseudonimiseringsrichtlijn, AVG/GDPR, JSON Schema, MIT, ECLI, BWBR) |

## Licentie

MIT — zie [LICENSE](LICENSE)

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md) (JREM open-source) voor bijdrage richtlijnen.

## Bronverwijzingen

- [Pseudonimiseringsrichtlijn — Rechtspraak.nl](https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn)
- [Wet griffierechten burgerlijke zaken (Wgbz) — wetten.overheid.nl](https://wetten.overheid.nl/BWBR0035817/)
- [Wet RO — wetten.overheid.nl](https://wetten.overheid.nl/BWBR0004701/)
- [Rechtspraak Open Data API — data.rechtspraak.nl](https://data.rechtspraak.nl/)

## Over Djimit Rules

JuraRegel is ontwikkeld door [Djimit Rules](https://github.com/djimit) als onderdeel van het Legal RuleOps Platform. De Rechtspraak is het pilot-domein. JuraRegel is herbruikbaar bij elke overheidsorganisatie die met administratief-juridische regels werkt.

