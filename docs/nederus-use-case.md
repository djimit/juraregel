# NEDERUS Use Case — Multi-Jurisdictional AI Compliance Mapping

## User Story

**Als** compliance officer bij een overheidsorganisie **wil ik** één set controls die tegelijkertijd voldoet aan EU AI Act, BIO2, NIS2 en NORA **zodat** ik niet vier aparte compliance-processen hoef te draaien.

## Wat NEDERUS is

NEDERUS (Nederlandse Unified AI Standards) is een **mapping-framework**, geen regelframework. Het bestaat niet naast JuraRegel — het **verbindt** de bestaande JuraRegel use cases:

```
JuraRegel (regels per framework)
    ├── EU AI Act use case (12 regels)
    ├── BIO2 use case (162 regels)
    ├── NIS2 use case (melding playbook)
    └── NORA use case (15 principes)

NEDERUS (mapping tussen frameworks)
    ├── NED-01: EU AI Act Art. 9 + BIO2 A.5-6 + NIS2 Art. 21 + NORA Grondslag
    ├── NED-02: EU AI Act Art. 10 + NORA Evenredigheid
    ├── NED-03: EU AI Act Art. 14 + NORA Proportionaliteit
    ├── NED-04: EU AI Act Art. 13/50 + NORA Openbaarheid
    └── NED-05: EU AI Act Art. 72 + BIO2 C.6-7 + NIS2 Art. 23
```

## Architectuur

```
┌─────────────────────────────────────────────────────────┐
│                    JuraRegel                             │
│  ┌─────────┐ ┌──────┐ ┌──────┐ ┌──────┐                │
│  │EU AI Act│ │ BIO2 │ │ NIS2 │ │ NORA │                │
│  │ :8498   │ │ :8494│ │ :8501│ │ :8497│                │
│  └────┬────┘ └──┬───┘ └──┬───┘ └──┬───┘                │
│       │         │        │        │                      │
│       └─────────┴────────┴────────┘                      │
│                  │                                       │
│            NEDERUS Layer                                 │
│       ┌─────────┴─────────┐                              │
│       │ 5 Unified Controls │                              │
│       │ NED-01 t/m NED-05  │                              │
│       └───────────────────┘                              │
└─────────────────────────────────────────────────────────┘
```

## De 5 NEDERUS Controls

### NED-01: AI Impact Assessment (HIGH)

Eén impact assessment die vier frameworks dekt:

| Framework | Artikel | Wat |
|-----------|---------|-----|
| EU AI Act | Art. 9(2), Art. 27 | Risicobeheersysteem + FRIA |
| BIO2 | A.5-6 | Risicoanalyse en -behandeling |
| NIS2 | Art. 21 | Risk management measures |
| NORA | Grondslag-toets | Beoordeling grondslag |

**JuraRegel integratie**: `POST /v1/eu-ai-act/classify` + `POST /v1/bio2/calculate`

### NED-02: Bias & Fairness Testing (HIGH)

| Framework | Artikel | Wat |
|-----------|---------|-----|
| EU AI Act | Art. 10 | Data governance + bias monitoring |
| NORA | Evenredigheid | AI-besluiten mogen niet discrimineren |

**JuraRegel integratie**: Via JREM regels in EU AI Act use case

### NED-03: Human Oversight (HIGH)

| Framework | Artikel | Wat |
|-----------|---------|-----|
| EU AI Act | Art. 14 | Human oversight measures |
| NORA | Proportionaliteit | Menselijke tussenkomst |

**JuraRegel integratie**: Via JREM regels in EU AI Act use case

### NED-04: Transparency & Explainability (MEDIUM)

| Framework | Artikel | Wat |
|-----------|---------|-----|
| EU AI Act | Art. 13, Art. 50 | Transparency obligations |
| NORA | Openbaarheid | Transparantie over AI-besluitvorming |

**JuraRegel integratie**: Via JREM regels in EU AI Act use case

### NED-05: Incident Response & Reporting (HIGH)

| Framework | Artikel | Timeline | Conflict |
|-----------|---------|----------|----------|
| EU AI Act | Art. 72 | 15 days initial | Resolved: apply most stringent |
| BIO2 | C.6-7 | Per BIO2 process | — |
| NIS2 | Art. 23 | 24h preliminary | Most stringent applies |

**JuraRegel integratie**: `POST /v1/nis2/calculate` + `POST /v1/bio2/calculate`

## MCP Server Integratie

De NEDERUS mapping wordt beschikbaar gemaakt via de JuraRegel MCP server:

| MCP Tool | Functie |
|----------|---------|
| `nederus_list_controls` | Lijst alle 5 NEDERUS controls met framework mapping |
| `nederus_get_control` | Detail van één control (NED-01 t/m NED-05) |
| `nederus_map_framework` | Geef alle controls voor een specifiek framework |
| `nederus_crosswalk` | Volledige crosswalk tussen twee frameworks |

Zie [nederus-mcp-tools.md](nederus-mcp-tools.md) voor implementatiedetails.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|-----|----------|-----------|
| Compliance officer | 4 frameworks × eigen rapportage | NEDERUS: één rapport, vier dekkingen |
| CISO | BIO2 + NIS2 overlappen maar andere terminologie | NEDERUS toont exacte overlap |
| Enterprise architect | NORA niet gekoppeld aan EU AI Act | NEDERUS koppelt principes aan artikelen |
| AI developer | Onbekend of AI aan alle kaders voldoet | NED-01 t/m NED-05 als startpunt |

## eIDAS Integratie

eIDAS raakt NEDERUS op het snijvlak van identiteit en AI:

| NEDERUS Control | eIDAS Koppeling | JuraRegel Use Case |
|---|---|---|
| NED-01 AI Impact Assessment | EID-006: Wallet impact verplicht | `use-cases/eidas/` |
| NED-03 Human Oversight | EID-006: Wallet vereist menselijke controle | `use-cases/eidas/` |
| NED-04 Transparency | EID-015: Attribuut-uitwisseling | `use-cases/eidas/` |
| NED-05 Incident Response | EID-009: Wallet deadline = hoog risico | `use-cases/eidas/` |
| NED-06 Secure Development | EID-006: Wallet = digitaal product | `use-cases/eidas/` |

Zie [eIDAS crosswalk](../openspec/changes/nederus-framework-v1/sources/crosswalks/eidas.md) voor de volledige mapping.

## Zie Ook

- [NEDERUS repository](https://github.com/djimit/nederus-framework) — controls.yaml, crosswalks, validation
- [NEDERUS proposal](../openspec/changes/nederus-framework-v1/proposal.md) — strategische rationale
- [NEDERUS design](../openspec/changes/nederus-framework-v1/design.md) — technische architectuur
- [eIDAS use case](eidas-use-case.md) — 20 regels, port 8523
