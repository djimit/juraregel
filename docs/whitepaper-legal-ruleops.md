# Legal RuleOps: From PDFs to APIs

## Hoe Nederlandse overheidsregels digitaal, testbaar en uitlegbaar worden

---

## 1. Het probleem

De Nederlandse overheid werkt met honderden administratief-juridische regels — van griffierecht tot BIO2, van Forum Standaardisatie tot EU AI Act. Deze regels staan in PDFs, wetten, regelingen en Markdown. Ze zijn leesbaar voor juristen maar niet uitvoerbaar door computers. Het resultaat: handmatige compliance checks, foutgevoelige spreadsheets, en onduidelijke verantwoording.

Onze analyse van 174.210 uitspraken toonde 25.127 uitspraken aan waarin persoonsgegevens werden gedetecteerd — 14,4% van de database. De pseudonimiseringsrichtlijn engine (V4.2) toonde aan dat naar schatting 59% hiervan false positives zijn onder de richtlijn. Het werkelijke aantal violations wordt geschat op ~18.000.

## 2. De oplossing: Legal RuleOps

**JuraRegel** is een open-source platform dat administratief-juridische regels vertaalt naar digitale, testbare, auditeerbare regels. Niet AI. Niet automatische beslissingen. Maar: regels die door juristen geschreven worden in leesbare taal (RegelSpraak CNL), door computers uitgevoerd worden (JREM), en door burgers begrepen worden (uitleg met bronverwijzing).

## 3. Het bewijs: 10 use cases, 7 domeinen

| Domein | Use cases | Regels | Poort |
|---|---|---|---|
| Rechtspraak | Griffierecht, Procesreglement, Classificatie, Publicatie/PII | 46 | 8490-8493 |
| Informatiebeveiliging | BIO2 (162 maatregelen, ISO 27002) | 162 | 8494 |
| Interoperabiliteit | Forum Standaardisatie (22 standaarden) | 22 | 8495 |
| Technische regels | Logius API Design Rules, OAuth, CloudEvents, Digikoppeling | 24 | 8496 |
| Architectuur | NORA (15 principes, meta-laag) | 15 | 8497 |
| AI Regulering | EU AI Act (12 regels) | 12 | 8498 |
| Privacy | AVG/GDPR (10 regels) | 10 | 8499 |
| **Totaal** | **10 use cases** | **291** | **8490-8499** |

## 4. De architectuur

```
Bron (PDF/Markdown/Wet) → RegelSpraak CNL → JREM (JSON Schema 2020-12)
  → CI/CD (14 gates) → Rule API (FastAPI) → Consumers (SDK/Dashboard/Portaal)
```

Elke use case volgt dezelfde pipeline. De factory pattern (`create_app(domain, jrem_path, port)`) maakt het schaalbaar.

## 5. Product Features

- **TypeScript SDK** — `npm install @juraregel/sdk` met typed clients
- **CLI** — `npx juraregel init <domein> <port>` scaffold nieuwe use cases
- **Docker** — `docker compose up` start alle 10 APIs
- **GitHub Actions** — reusable CI workflow
- **Dashboard** — visueel overzicht met live health checks
- **JREM open standaard** — MIT license, JSON Schema 2020-12

## 6. De standaard: JREM open-source

JREM (Judicial Rule Exchange Model) is een open JSON Schema dat juridische regels structureert met bronverwijzingen, versiebeheer en jurist-acceptatie. MIT license op GitHub.

## 7. De pitch

> "JuraRegel vertaalt bijvoorbeeld de pseudonimiseringsrichtlijn van Rechtspraak.nl en andere juridische richtlijnen naar digitale, testbare, auditeerbare regels. 10 use cases, 7 domeinen, 291 regels, 207 tests. Open-source. TypeScript SDK. Docker. GitHub Actions. Voor juristen, ontwikkelaars, en burgers."

## 8. Validatie

| Metriek | Waarde |
|---|---|
| Use cases | 10 |
| JREM regels | 291 |
| Tests | 207 (alle groen) |
| CI gates | 14 per use case |
| Pseudonimisering engine | V4.2 — 100% op 25.127 uitspraken |
| Open standaarden | 7 compliant |
| GitHub | github.com/djimit/juraregel |
| Djimitflo | 189 LROP entries, 13 learning cycles |

---

*JuraRegel v1.0.0 — juli 2026 — github.com/djimit/juraregel — MIT license*
