# Eindoordeel: JuraRegel v2.1 Hardening

**Datum:** 5 juli 2026
**Opdrachtgever:** Dennis Landman
**Rol:** Criticus als overheidsjurist, CISO, AI-ethicus, productowner

---

## Samenvatting

JuraRegel is een **ambitieus concept** met een **solide technische basis**, maar de repository lijdt aan **overgeclaimde documentatie**, **optische CI**, en **structurele inconsistenties** die het platform ongeschikt maken voor productiegebruik in een overheidscontext.

**Score: 5,5 / 10**

---

## Wat is goed

### 1. Visie en architectuur
Het idee om juridische regels te vertalen naar versieerbare, testbare, uitlegbare rule artifacts is sterk. JREM als uitwisselmodel is logisch en de basisvelden (geldigheidsperiode, bronverwijzingen, conditions, outcome) zijn passend voor legal engineering.

### 2. Griffierecht use case
De beste use case. Echte rule-as-code discipline: JREM exports met schemaVersion, bronverwijzingen, concrete condities, deterministische outcomes en voorbeelden. Dit is het patroon dat je wilt voor legal engineering.

### 3. Testopzet griffierecht
Inhoudelijk volwassen voor een PoC: happy path, negatieve cases, boundary tests, regressie tussen versies, explainability, audit en embedded JREM-scenario's.

### 4. Pseudonimiseringsrichtlijn-engine
Raakt een reëel probleem. De onderscheid tussen natuurlijke personen, professioneel betrokken personen, rechtspersonen en overheidsorganisaties is conceptueel relevant.

### 5. MCP Server
Goed gedesignd protocol met resources en prompts (niet alleen tools). De architectuur is modern en agent-vriendelijk.

### 6. BDD Tests
Gherkin scenarios die door juristen leesbaar zijn. Goed startpunt voor legal acceptance pipeline.

---

## Wat is zwak

### 1. Juridische accordering is waardeloos
Elke use case bevat `"self-approved-poC"` door de maker zelf. Dit is juridisch niet houdbaar. Een notaris kan zijn eigen akte niet accorderen.

### 2. CI/CD is optisch
`|| true` onderdrukt alle failures in de GitHub Actions workflow en `run-all-gates.sh`. Pipelines slagen optisch terwijl onderliggende validaties falen. **Dit ondermijnt het hele kwaliteitsmodel.**

### 3. JREM schema is inconsistent
- `$id` in v1.1.0 verwijst naar v1.0.0
- `outcome` vereist griffierecht-specifieke velden (niet generiek)
- `description` verwijst naar verkeerde versie
- Migratie tool is heuristiek, geen transformatie

### 4. Security is een façade
- "Auth" accepteert elk niet-leeg bearer token
- CORS staat open voor alle origins
- Geen audit logging
- Geen SECURITY.md (nu wel toegevoegd)

### 5. Overgeclaimde documentatie
- "100% nauwkeurigheid op 25.127 uitspraken" — niet onafhankelijk gevalideerd
- "451 tests" — inclusief stubs en niet-functionele tests
- "Productie-ready" — niet aantoonbaar
- "ENSIA aligned" — niet gedefinieerd

### 6. Scope sprawl
28 use cases, geen enkele productie-ready. Griffierecht is solide, de rest zijn stubs of half-producten.

### 7. BIO2 en compliance use cases
Geen echte compliance engines. BIO2 geeft 0% compliance omdat de tool geen evidence leest. Forum Standaardisatie geeft scores zonder projectcontext.

### 8. Connectors zijn non-functioneel
`sources/bwb_connector.py` en andere connectors bevatten alleen `pass` statements.

### 9. Hardcoded data
- Bedragen in JREM exports (123 euro)
- Timestamps in API responses
- `hash()` voor audit (niet-deterministisch)

### 10. Geen gebruikersdocumentatie
Geen "Getting Started", geen "Rule Authoring", geen "Legal Review" handleidingen.

---

## Geïntegreerde bevindingen uit beide reviews

### Externe criticus vs Interne review

| Onderwerp | Externe score | Interne score | consensus |
|-----------|--------------|---------------|-----------|
| Juridische accordering | Kritiek | Kritiek | ✅ Beide |
| CI/CD || true | Kritiek | Kritiek | ✅ Beide |
| JREM schema | Kritiek ($id bug) | Kritiek | ✅ Beide |
| Security | Kritiek (auth façade) | Kritiek | ✅ Beide |
| Overgeclaimde claims | Kritiek | Kritiek | ✅ Beide |
| Scope sprawl | Kritiek | Kritiek | ✅ Beide |
| Griffierecht | Goed | Goed | ✅ Beide |
| MCP Server | Goed | Goed | ✅ Beide |
| BDD Tests | Niet genoemd | Goed | ➕ Intern |
| BIO2/Compliance | Kritiek | Kritiek | ✅ Beide |
| Connectors | Niet genoemd | Kritiek (stubs) | ➕ Intern |
| Documentatie inconsistentie | Kritiek (dubbel) | Niet genoemd | ➕ Extern |

### Unieke externe bevindingen
- README bevat dubbele statistieken (4 use cases vs 28 use cases)
- CLI (`bin/juraregel.mjs`) heeft syntax errors
- Dockerfile expose mismatch met Docker Compose
- BIO2 versie is verouderd (2025.1 vs actueel v1.3)
- Geen PR's, geen branch protection
- Geen CodeQL, Dependabot, secret scanning

### Unieke interne bevindingen
- Sources/connectors volledig non-functioneel
- MCP server zonder auth/audit
- Governance registry statisch
- Geen versiebeheer voor regels

---

## Wat is gefixt in v2.1.1

| Issue | Status |
|-------|--------|
| `|| true` in CI workflow | ✅ Gefixt |
| `|| true` in run-all-gates.sh | ✅ Gefixt |
| "100%" claims in README | ✅ Gefixt |
| README disclaimer | ✅ Toegevoegd |
| JREM v1.1.0 `$id` | ✅ Gefixt |
| JREM v1.1.0 description | ✅ Gefixt |
| JREM outcome required fields | ✅ Gefixt |
| SECURITY.md | ✅ Toegevoegd |

## Wat moet nog gebeuren (OpenSpec plan)

| Prioriteit | Issue | Inspanning |
|-----------|-------|------------|
| 1 | Juristische accordering herzien | 1-2 weken |
| 2 | Bronverwijzingen verplichten (bwbId, versie) | 2-4 weken |
| 3 | Scope reductie (3 active, rest stub) | 1 week |
| 4 | Security hardening (auth, CORS) | 1 week |
| 5 | Gebruikersdocumentatie | 1-2 weken |
| 6 | Connector implementatie | 2-4 weken |
| 7 | CLI fix | 1 dag |
| 8 | Dockerfile fix | 1 dag |

---

## Advies per doelgroep

### Voor juristen en legal engineers
**Nuttig als** denkmodel en rule-extraction prototype. **Niet gebruiken** zonder menselijke juridische validatie. Start met griffierecht.

### Voor architecten
**Interessant als** referentie voor "legal rules as code". **Niet als blauwdruk** voor productie zonder herarchitectuur.

### Voor CISO's en compliance officers
**Bruikbaar als** demo voor evidence-driven compliance. De BIO2, NCSC en Forum-modules leveren **geen betrouwbare compliance evidence**.

### Voor developers
**Leerzaam**, vooral griffierecht en FastAPI-factory. SDK, CLI, Docker en CI moeten **eerst gerepareerd**.

### Voor overheidsorganisaten
**Geschikt voor** innovatiepilot of sandbox. **Niet voor** formele besluitvorming of burgerinteractie.

---

## Conclusie

JuraRegel is een **veelbelovend concept** met een **bruikbare kern**, maar de repository is momenteel meer visie + PoC + gegenereerde uitbreidingen dan betrouwbaar product.

**Mijn advies: niet stoppen, wel radicaal versmallen en verharden.**

1. Kies twee domeinen voor diepte: griffierecht en pseudonimiseren
2. Maak CI echt hard (geen `|| true`)
3. Saner claims in documentatie
4. Voeg onafhankelijke juridische validatie toe
5. Pas dan opschalen naar BIO2, AVG, AI Act

De technische stack is geschikt. De ambitie is groot. Maar de kwaliteitsgovernance moet groeien met de scope.

**Score: 5,5/10** — Goed voor PoC, onvoldoende voor productie.
