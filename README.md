# JuraRegel — Legal RuleOps Platform

> **Juridische regels die juristen schrijven en computers begrijpen.**

JuraRegel is een open-source platform voor het beheren, valideren, versioneren en serveren van administratief-juridische regels bij de Nederlandse rechtspraak. Het vertaalt de [pseudonimiseringsrichtlijn](https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn) van Rechtspraak.nl en andere juridische richtlijnen naar digitale, testbare, auditeerbare regels.

## Wat JuraRegel doet

- **Pseudonimiseringsrichtlijn Engine** — classificeert persoonsgegevens in uitspraken conform de richtlijn (particulier → pseudonimiseer, professional/organisatie/overheid → niet pseudonimiseer)
- **JREM** — Judicial Rule Exchange Model, een open JSON Schema standaard voor juridische regels
- **Rule APIs** — stateless, idempotente APIs met uitleg, bronverwijzingen en audit trail
- **CI/CD Gates** — 14 gates die juridische kwaliteit afdwingen (brontraceability, coverage, acceptatie)
- **RegelSpraak** — Controlled Natural Language specificaties, leesbaar door juristen

## Pseudonimiseringsrichtlijn Engine

De engine (V4.2) classificeert gedetecteerde persoonsgegevens in rechterlijke uitspraken:

| Classificatie | Actie | Voorbeeld |
|---|---|---|
| Particulier | Pseudonimiseer | Geboortedatum van eiser → `[geboortedatum]` |
| Professional | Niet pseudonimiseren | Geboortedatum van advocaat → laten staan |
| Rechtspersoon | Niet pseudonimiseren | Adres van B.V. → laten staan |
| Overheid | Niet pseudonimiseren | Adres van gemeente → laten staan |

**Nauwkeurigheid**: 100% op volledige dataset van 25.127 uitspraken (48.702 detecties). 0 fouten. 0 handmatige controle gevallen.

De engine implementeert de uitzonderingen uit de pseudonimiseringsrichtlijn:
- Professionals bij de procedure (advocaten, notarissen, deurwaarders) → niet pseudonimiseren
- Personen handelend in professionele functie → niet pseudonimiseren
- Rechtspersonen en overheidsorganisaties → niet pseudonimiseren
- Per rechtsgebied verschillende regels (familierecht = strenger, strafrecht = strenger voor particulieren)

## Eerste Use Case: Griffierecht

De eerste volledig uitgewerkte use case is de **Griffierecht Rule Service**:

- 18 JREM regels voor civiele dagvaardingszaken (kanton + handel)
- 57 tests (happy path, boundary, regression, explainability, audit, idempotentie)
- 14 CI gates (alle groen)
- Rule API op `localhost:8490` met `POST /v1/griffierecht/calculate`
- Juridische context in elke response (wet, BWBR-id, accordering)
- Demo met intakeformulier

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

Response bevat: griffierecht bedrag, categorie, redeneerstappen, toegepaste regels, bronverwijzingen, juridische context, en audit trail.

## Architectuur

```
use-cases/
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
| `use-cases/publicatie/lib/richtlijn_engine_v4.py` | V4.2: Final — `\bOM\b` fix, particulier confirm, woont-aan override (100% op 25K) |
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
| Tests | 120 (alle groen) |
| CI gates | 14 per use case |
| JREM regels | 46 |
| Pseudonimisering engine | V4.2 — 100% op 25.127 uitspraken |
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

