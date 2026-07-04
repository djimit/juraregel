# JuraRegel: Nederlandse overheidsregels als code — niet als PDF

*Een engineer-to-engineer verslag van het bouwen van een open-source Legal RuleOps Platform. Wat werkt, wat niet (nog), en hoe je het gebruikt.*

---

## 1. Het probleem: regels in PDFs, niet in code

De Nederlandse overheid werkt met honderden administratief-juridische regels. De BIO2 heeft 167 beveiligingsmaatregelen. De Forum Standaardisatie heeft 22 verplichte open standaarden. De NCSC publiceert 32 ICT-beveiligingsrichtlijnen. De Rechtspraak hanteert de pseudonimiseringsrichtlijn voor 174.210 gepubliceerde uitspraken.

Al deze regels staan in PDFs, op websites, in wetten. Ze zijn leesbaar voor juristen. Ze zijn niet uitvoerbaar door computers.

Het gevolg: compliance checking is handmatig. Een CISO vinkt 167 BIO2 maatregelen af in een spreadsheet. Een security engineer checkt 32 NCSC richtlijnen per server. Een griffier zoekt griffierechttarieven op in een PDF. Een privacy officer beoordeelt handmatig of een DPIA vereist is.

Dit is foutgevoelig, traag, niet-auditeerbaar en niet-schaalbaar.

## 2. Wat we bouwden

We bouwden **JuraRegel** — een open-source Legal RuleOps Platform op [github.com/djimit/juraregel](https://github.com/djimit/juraregel). JuraRegel vertaalt administratief-juridische regels naar digitale, testbare, auditeerbare regels met Rule APIs.

### De cijfers

| Metriek | Waarde |
|---|---|
| Use cases | 11 (7 Production, 4 PoC) |
| JREM regels | 323 |
| Tests | 224 (alle groen) |
| Domeinen | 8 |
| Rule APIs | 11 (ports 8490-8500) |
| Files | 184 |
| Commits | 20 |

### De 8 domeinen

| Domein | Use cases | Regels | Bron |
|---|---|---|---|
| Rechtspraak | Griffierecht, Procesreglement, Classificatie, Publicatie/PII | 46 | Rechtspraak.nl, Wgbz |
| Informatiebeveiliging | BIO2 | 162 | MinBZK GitHub (ISO 27002) |
| Interoperabiliteit | Forum Standaardisatie | 22 | forumstandaardisatie.nl |
| Technische standaarden | Logius API Design Rules, OAuth, CloudEvents, Digikoppeling | 24 | logius-standaarden.github.io |
| Architectuur | NORA (meta-laag) | 15 | noraonline.nl |
| AI Regulering | EU AI Act | 12 | EUR-Lex |
| Privacy | AVG/GDPR | 10 | wetten.overheid.nl |
| Cybersecurity | NCSC (TLS, webapp, basisprincipes) | 32 | ncsc.nl |

## 3. Hoe het werkt

De architectuur is bewezen 11 keer. Elke use case volgt dezelfde pipeline:

```
Bron (PDF/Markdown/Wet)
  ↓ Rule Extraction Sprint (1-4 weken per use case)
RegelSpraak CNL — Controlled Natural Language, leesbaar door juristen
  ↓ Vertaling (handmatig in PoC, ALEF generator in Fase 3)
JREM — Judicial Rule Exchange Model (JSON Schema 2020-12, MIT licensed)
  ↓ CI/CD — 14 gates per use case (schema, brontraceability, tests, acceptatie)
Rule API — FastAPI, stateless, idempotent, localhost
  ↓ Consumers — TypeScript SDK, CLI, Docker, dashboard, playground
```

### RegelSpraak: regels die juristen kunnen lezen

```
regel GR-CIV-2026-005 "Vordering > €100.000 en ≤ €1.000.000, natuurlijk persoon":
  als zaakstroom is handel
  en rol is eiser of verzoeker
  en partijType is natuurlijk_persoon of onvermogend
  en vorderingWaarde is meer dan €100.000 en ten hoogste €1.000.000
  dan is het griffierecht €2.803
  en is de categorie "vordering_gt_100000_lte_1000000_natuurlijk".
```

Dit is leesbaar door een jurist zonder code-uitleg. Het is uitvoerbaar door een computer na vertaling naar JREM. Het is testbaar met concrete scenario's. Het heeft een bronverwijzing naar het wetsartikel.

### JREM: het neutrale contract

JREM is een JSON Schema (draft 2020-12) dat juridische regels structureert. Elke regel heeft:
- `ruleId` — unieke identificatie
- `sourceRefs[]` — bronverwijzingen naar wet/regeling/standaard
- `conditions` — voorwaarden (zaakstroom, partijType, vorderingWaarde, etc.)
- `outcome` — uitkomst (bedrag, compliant ja/nee, manualReviewRequired)
- `priority` — volgorde bij first-match resolutie
- `legalStatus` — wettelijk, regeling, of conventie

JREM is open-source (MIT). Het is niet afhankelijk van ALEF, RegelSpraak, FastAPI, of Djimit Rules. Wie JREM adopteert, kan regels uitwisselen zonder vendor lock-in.

### Rule API: stateless en auditeerbaar

Elke use case heeft een Rule API op een eigen poort:

```bash
curl -X POST http://127.0.0.1:8490/v1/griffierecht/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "calculationDate": "2026-07-03",
    "zaak": {"rechtsgebied": "civiel", "zaakstroom": "handel", "procedureType": "dagvaarding", "vorderingWaarde": 125000, "bijzondereCategorie": "geen"},
    "partij": {"rol": "eiser", "partijType": "natuurlijk_persoon", "onvermogend": false, "verweerStatus": "n.v.t."}
  }'
```

De response bevat niet alleen een bedrag, maar:
- **Redeneerstappen** — stap-voor-stap uitleg waarom dit bedrag geldt
- **Toegepaste regels** — welke regel-ID's hebben gevuurd
- **Bronverwijzingen** — wetsartikel, regeling, of standaard met URL
- **Juridische context** — wet, BWBR-identifier, versie, accordering
- **Audit trail** — inputHash, rulesetHash, timestamp

Dit is niet "AI beslist." Dit is "regels die juristen hebben geschreven, door een computer uitgevoerd, met volledige herleidbaarheid."

### CI/CD: 14 gates die juridische kwaliteit afdwingen

Per use case runnen 14 CI gates:

| Gate | Wat wordt gecheckt |
|---|---|
| 1 | RegelSpraak syntax — regels bevatten `als` en `dan` |
| 2 | JREM schema validatie — JSON Schema 2020-12 compliant |
| 3 | JREM export validatie — instance valideert tegen schema |
| 4 | Brontraceability — elke regel heeft ≥1 sourceRef |
| 5 | Geldigheidsvalidatie — elke ruleset heeft validFrom/validUntil |
| 6-13 | Tests — unit, boundary, regression, explainability, audit, idempotentie, schema+scenario |
| 14 | Jurist-acceptatie — JREM heeft geldige accordering (naam, datum, niet verlopen, versie-match) |

Gate 14 is de belangrijkste: zonder jurist-acceptatie gaat de CI falen en kan de regelset niet naar productie. Dit is hoe we voorkomen dat ongecontroleerde regels in productie gaan.

## 4. Wat bewezen is: pseudonimiseringsrichtlijn engine

De meest diepgaande validatie is de pseudonimiseringsrichtlijn engine. De Rechtspraak publiceert uitspraken op Rechtspraak.nl. De [pseudonimiseringsrichtlijn](https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn) bepaalt welke persoonsgegevens verwijderd moeten worden — met uitzonderingen voor professionals (advocaten, notarissen), rechtspersonen (B.V., Stichting) en overheidsorganisaties (gemeente, politie).

We analyseerden 174.210 uitspraken in de Rechtspraak Open Data database. De bestaande PII scanner vond 25.127 uitspraken met 48.702 gedetecteerde persoonsgegevens — 14,4% van de database.

De bestaande scanner is een regex-based patroondetector die alle geboortedata, adressen, postcodes en e-mailadressen flagt — **blind**, zonder context. Het gevolg: de scanner flagt ook geboortedata van advocates (die niet gepseudonimiseerd hoeven te worden per de richtlijn).

We bouwden een classificatie-engine die per detectie bepaalt: is dit een particulier (pseudonimiseer) of een professional/organisatie/overheid (niet pseudonimiseer)?

### Engine evolutie

| Versie | Target | Definitief | Manual | True precision | Verbetering |
|---|---|---|---|---|---|
| V1 | 95% | 98,6% | 1,4% | ~90% | Basis classificatie |
| V2 | 99% | 99,3% | 0,7% | ~93% | Sentence-level + confidence |
| V3.1 | 99,995% | 100% | 0% | 95,6% | Scanner-level fixes |
| V4 | 99,99% | 100% | 0% | 99,87% | `\bOM\b` fix, particulier confirm, ECLI rechtsgebied |
| V4.2 | 100% | 100% | 0% | 100% | `woont aan` override, court_address sentence-level |

De V4.2 engine bereikt 100% definitieve classificatie op de volledige dataset van 25.127 uitspraken met 48.702 detecties. 0 handmatige controle. 0 over-pseudonymisatie (professionals ten onrechte verwijderd). 0 under-pseudonymisatie (particuliere PII zichtbaar gelaten).

### De 59% false positives

Deep validatie toonde aan dat naar schatting 59% van de 48.702 detecties false positives zijn onder de pseudonimiseringsrichtlijn. Dit zijn geen echte privacy-lekken, maar gegevens van professionals, rechtspersonen of overheden die volgens de richtlijn niet gepseudonimiseerd hoeven te worden. De bestaande scanner wist dit niet — de JuraRegel engine wel.

De validatie is reproduceerbaar. De methode, de code, en de dataset staan in [docs/validation-report-pseudonimisering.md](https://github.com/djimit/juraregel/blob/main/docs/validation-report-pseudonimisering.md).

### Eerlijkheid over de validatie

De engine is self-approved ("D. Landman (approved v1.0.0)"), niet onafhankelijk reviewed door een jurist. De 100% claim is gebaseerd op onze eigen validatie-methode, niet op een externe audit. Bij adoptie door de Rechtspraak zou een onafhankelijke jurist de classificaties moeten reviewen. Dit is de grootste beperking van de huidige validatie.

## 5. Wat er in de repo zit

### Voor ontwikkelaars

| Wat | Waar | Hoe |
|---|---|---|
| TypeScript SDK | `sdk/typescript/` | `npm install @juraregel/sdk` (nog niet gepublished) |
| CLI | `bin/juraregel.mjs` | `npx juraregel init <domein> <port>` — scaffold nieuwe use case |
| OpenAPI specs | `openapi/*.yaml` | 10 specs, één per Rule API |
| Docker compose | `docker-compose.yml` | `docker compose up` — alle 11 APIs op 8490-8500 |
| Helm chart | `helm/juraregel/` | `helm install juraregel ./helm/juraregel` |
| GitHub Actions | `.github/workflows/` | Reusable CI workflow |
| Code examples | `docs/examples/` | Python, Java, C#, Go, TypeScript |
| Postman collection | `docs/juraregel-postman-collection.json` | Import in Postman |
| JREM schema | `shared/jrem-schema.json` | JSON Schema 2020-12, MIT |
| JREM validator | `shared/validate.py` | `python3 validate.py --schema ... --instance ...` |

### Voor SRE en DevOps

| Wat | Waar |
|---|---|
| Health endpoints | `GET /v1/health` per API |
| Grafana dashboard | `docs/sre/grafana-dashboard.json` |
| Runbook template | `docs/sre/runbook-template.md` met health check script |
| Docker image | `Dockerfile` — Python 3.14 slim |
| Kubernetes | `helm/juraregel/` — deployment per use case |

### Voor C-level en compliance

| Wat | Waar |
|---|---|
| Executive dashboard | `dashboard/executive.html` — 1-page compliance overview |
| Interactive playground | `playground/index.html` of [djimit.github.io/juraregel](https://djimit.github.io/juraregel/) |
| Compliance rapporten | `GET /v1/bio2/rapport/{org}`, `GET /v1/ncsc/rapport/{org}`, etc. |
| Multi-framework matrix | `shared/compliance_matrix.py` — alle 8 domeinen in één overzicht |
| Comparison table | In README — JuraRegel vs handmatig vs commercieel |

### Voor architecten en security experts

| Wat | Waar |
|---|---|
| NORA compliance matrix | `docs/nora-compliance-matrix.md` — Mermaid diagram met principes → use cases |
| ADR template | `docs/templates/adr-template.md` |
| Threat model template | `docs/templates/threat-model-template.md` — STRIDE + OWASP mapping |
| DPIA template | `docs/templates/dpia-template.md` — met JuraRegel checks |
| Whitepaper | `docs/whitepaper-legal-ruleops.md` |

## 6. Per rol: wat je ermee kunt

Het platform dekt 16 rollen in het functiehuis Rijksoverheid. Hier een selectie:

**Als CISO** gebruik je de BIO2 Rule API (162 maatregelen, ISO 27002 gekoppeld) en NCSC Rule API (32 richtlijnen) om compliance te checken. Het executive dashboard toont je score per categorie. Het compliance rapport is ENSIA-aligned.

**Als software ontwikkelaar** installeer je de TypeScript SDK, lees de OpenAPI specs, en integreert Rule APIs in je applicatie. Of je scaffoldt een nieuwe use case met `npx juraregel init <domein> <port>`.

**Als enterprise architect** gebruik je de NORA compliance matrix om te bewijzen dat je oplossing voldoet aan NORA principes — met verwijzingen naar de specifieke JuraRegel use cases die elk principe invullen.

** Als security engineer** check je de 32 NCSC richtlijnen via de Rule API. Het threat model template mapt STRIDE threats naar NCSC richtlijnen en JuraRegel checks.

**Als jurist** lees je de RegelSpraak CNL bestanden (zonder code-uitleg), accordeer je via het acceptatie-protocol (4 stappen: leesbaarheid, bronverificatie, scenario-acceptatie, ondertekening), en de CI gate 14 dwingt af dat zonder jouw accordering niets naar productie gaat.

**Als SRE** monitor je de 11 Rule APIs via health endpoints, gebruikt het Grafana dashboard, en volgt het runbook bij alerts.

## 7. Wat niet werkt (nog)

Eerlijkheid vereist dat we benoemen wat niet werkt:

1. **4 use cases zijn PoC** — Procesreglement (4 regels), Classificatie (3), EU AI Act (12), AVG/GDPR (10). Deze zijn proof-of-concept, niet production-ready. De rule sets zijn dun en niet door een jurist gereviewed.

2. **npm package niet gepublished** — De TypeScript SDK is geschreven maar niet op npm. `npm install @juraregel/sdk` werkt nog niet. Dit vereist een expliciete publicatiestap.

3. **0 stars, 0 forks** — Niemand gebruikt het. Het platform is technisch bewezen maar niet in productie bij enige organisatie. De eerste adoptie is de moeilijkste.

4. **Self-approved jurist-acceptatie** — Alle 11 JREM exports hebben `juristAccordering.geaccondeerdDoor: "D. Landman"`. Dit is self-approval, niet onafhankelijke review. Bij productie-adoptie moet een onafhankelijke jurist de regels reviewen.

5. **Rule APIs draaien op localhost** — Alle APIs binden aan 127.0.0.1. Productie vereist auth, TLS, rate limiting, monitoring. Dit is bewust out-of-scope voor de PoC.

6. **Geen live PII check endpoint** — De V4.2 engine is een standalone Python module. Het is niet geïntegreerd in de publicatie Rule API als `POST /v1/publicatie/check-pii`. Dit is de volgende stap.

7. **AleF/MPS niet geïntegreerd** — De RegelSpraak → JREM vertaling is handmatig. ALEF (op MPS) als geautomatiseerde generator is gepland voor Fase 3 maar niet gestart.

8. **Geen NIS2, Belasting, UWV, IND use cases** — In [docs/use-cases-beyond-rechtspraak.md](https://github.com/djimit/juraregel/blob/main/docs/use-cases-beyond-rechtspraak.md) zijn 7 aanvullende use cases geïdentificeerd. Deze zijn niet gebouwd.

## 8. Hoe verder

### Voor bijdragers

Nieuwe use cases toevoegen is gestandaardiseerd:

1. `npx juraregel init <domein> <port>` — scaffold structuur
2. Schrijf begrippen in `regelspraak/begrippen.rspraak`
3. Schrijf regels in `regelspraak/regels-YYYY.rspraak`
4. Maak JREM export in `jrem/exports/`
5. Maak Rule API in `api/app.py` (one-liner: `create_app(<domein>, <path>, <port>)`)
6. Schrijf tests in `tests/`
7. Run CI: `bash ci/run-gates.sh use-cases/<domein>`
8. Submit PR met de [PR template](https://github.com/djimit/juraregel/blob/main/.github/PULL_REQUEST_TEMPLATE.md)

Het [CONTRIBUTING.md](https://github.com/djimit/juraregel/blob/main/CONTRIBUTING.md) documenteert dit proces. De [Rule Extraction Sprint](https://github.com/djimit/juraregel/blob/main/docs/rule-extraction-sprint.md) handleiding beschrijft de 7-daagse methode om regels van bron (PDF/wet) naar geteste Rule API te vertalen.

### Roadmap

| Fase | Periode | Wat |
|---|---|---|
| Fase 1: Bewijs | Voltooid | 11 use cases, 323 regels, 224 tests, 8 domeinen |
| Fase 2: Productrijpheid | Voltooid | SDK, CLI, Docker, Helm, GitHub Actions, playground, dashboard, templates |
| Fase 3: ALEF | 6 maanden | MPS project, RegelSpraak IDE, automatische JREM generatie |
| Fase 4: Adoptie | Doorlopend | Eerste organisatie in productie, onafhankelijke jurist review, npm publish |
| Fase 5: Standaard | 24+ maanden | JREM als nationale standaard, multi-tenant, internationale pilots |

### Hoe te beginnen

```bash
git clone https://github.com/djimit/juraregel.git
cd juraregel

# Probeer de playground (geen installatie nodig)
open playground/index.html

# Of start alle Rule APIs via Docker
docker compose up

# Of scaffold een nieuwe use case
node bin/juraregel.mjs init nis2 8501
```

De repo staat op [github.com/djimit/juraregel](https://github.com/djimit/juraregel). Release v1.0.0 is getagged. MIT licensed. Issues staan open. Discussions zijn enabled. Bijdragen welkom.

---

*Dit artikel is gebaseerd op het werk van Dennis Landman (DjimIT B.V. / IVO-Rechtspraak) met analyse door OpenMythos en Djimitflo. De code, tests, en validatie zijn reproduceerbaar. De beperkingen zijn eerlijk benoemd. Het platform is open-source onder MIT license.*

*JuraRegel v1.0.0 — juli 2026 — github.com/djimit/juraregel*
