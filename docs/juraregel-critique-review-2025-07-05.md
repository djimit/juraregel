# Kritische Review — JuraRegel v2.1.0

**Datum:** 5 juli 2026
**Rol:** Criticus als overheidsjurist, informatiebeveiliger, AI-ethicus, en productowner
**Scope:** Volledige repository: JREM exports, MCP server, BDD tests, governance, documentatie

---

## Samenvatting

JuraRegel v2.1.0 is een indrukwekkende technische prestatie. De architectuur is solide, de tooling is modern, en de ambitie is groot. Maar vanuit de vier rollen die ik annam — jurist, CISO, AI-ethicus, productowner — zijn er **structurele zwaktes** die het platform onbruikbaar maken voor productiegebruik door de overheid. Dit document benoemt die zwaktes eerlijk en geeft aanpak.

**Kernboodschap:** JuraRegel is een mooie demo, maar nog geen overheidsplatform.

---

## 1. JURIDISCHE CRITICUS

### 1.1 Juristische Accordering is een Vrijbrief

**Probleem:**
```json
"juristAccordering": {
  "geaccondeerdDoor": "D. Landman",
  "datum": "2025-07-05",
  "status": "self-approved-poC",
  "onafhankelijk": false
}
```

Elke use case bevat deze accordering. De maker accordeert zijn eigen werk. Dit is juridisch waardeloos. Geen rechter, toezichthouder of acceptatiecommissie accepteert "self-approved-poC".

**Wat een jurist zegt:**
> "Dit is alsof een notaris zijn eigen akte tekent. De `onafhankelijk: false` is eerlijk, maar dat maakt het niet beter. Voor productie heb je een onafhankelijke jurist nodig."

**Aanpak:**
- Verwijder `juristAccordering` uit exports, of
- Voeg `accorderingType` toe: `["self", "peer-review", "legal-team", "external"]`
- Blokkeer productie-deploy als `accorderingType` niet minimaal `"legal-team"` is

### 1.2 Bronverwijzingen zijn Oppervlakkig

**Probleem:**
```json
"sourceRefs": [{"type": "wet", "title": "Toeslagenwet", "section": "art. 8"}]
```

Dit verwijst naar "art. 8". Maar: welk lid? Welke versie? Is de verwijzing nog actueel?

**Wat een wetgevingsjurist zegt:**
> "'art. 8' is geen bruikbare bronverwijzing. Je moet minimaal hebben: artikel, lid, onderdeel, en de versie van de wet. Idealiter met BWB-identifier en versiedatum."

**Aanpak:**
- Verplicht `bwbId` in sourceRefs (deels gedaan in v1.1.0)
- Voeg `wetVersie` toe: datum van de gebruikte versie
- Voeg `lid` en `onderdeel` toe als aparte velden
- EIS: elke regel traceerbaar naar specifieke wettekst op specifieke datum

### 1.3 Outcome Bedragen zijn Static en Onverifieerbaar

**Probleem:**
```json
"outcome": {"bedrag": {"amount": 123, "currency": "EUR", "periode": "maandelijks"}}
```

Het bedrag 123 euro is hardcoded. De daadwerkelijke zorgtoeslag wordt jaarlijks vastgesteld via het Besluit zorgtoeslag.

**Wat een bestuursjurist zegt:**
> "Een hardcoded bedrag in JSON heeft geen juridische status. De Belastingdienst publiceert jaarlijks nieuwe bedragen. Als iemand besluit op basis van dit bedrag, is dat niet houdbaar — en jij bent aansprakelijk."

**Aanpak:**
- Verwijder hardcoded bedragen; gebruik alleen `recht: true/false`
- Bedragen ophalen uit externe, beheerde bron
- Voeg `bedragBron` en `bedragDatum` toe als metadata

### 1.4 ProcedureType is Inconsistent

**Probleem:**
`"procedureType"` waarden variëren wild: `"toeslagen-berekening"`, `"dagvaarding"` (BIO2 is geen procedure!), `"classificatie"`, `"publicatie"`.

**Aanpak:**
- Definieer gesloten lijst van procedureTypes
- Valideer in CI gate
- Geef elke type een definitie

### 1.5 "Deterministic" is een Leugen

**Probleem:**
Elke regel heeft `"confidence": "deterministic"`. Maar de regels zijn geïnterpreteerd door een programmeerder met LLM-hulp.

**Wat een rechtsgeleerde zegt:**
> "Deterministisch betekent: dezelfde input = altijd dezelfde output. Maar de vertaling van wet naar regel is interpretatie. Je claims deterministisch te zijn, maar je bent 'volgens interpretatie van de maker'."

**Aanpak:**
- Vervang `"deterministic"` door `"interpretatie"` of `"volgens-bron"`
- Voeg `interpretatieOpmerking` toe

---

## 2. INFORMATIEVEILIGING & ARCHITECTUUR CRITICUS

### 2.1 MCP Server draait via stdio — Geen Authenticatie

**Probleem:**
Geen authenticatie, autorisatie, rate limiting, of audit logging.

**Wat een CISO zegt:**
> "Elke process op deze machine kan deze MCP server aanroepen. Zonder audit trail weet je niet wie wat heeft opgevraagd."

**Aanpak:**
- Voeg authenticatie toe (API key of OAuth)
- Audit logging: elke tool call gelogd
- Rate limiting

### 2.2 Qdrant en SQLite — Geen Backup Strategy

**Probleem:**
`.qdrant/` en `.keyword.db` staan in `.gitignore`. Bij data verlies is alles weg.

**Aanpak:**
- Documenteer backup procedure
- Voeg export/import script toe

### 2.3 Schema Versioning is Incompleet

**Probleem:**
- `$id` in v1.1.0 verwijst nog naar `v1.0.0` (bug)
- Geen echte JSON Schema validatie in CI
- Migratie is heuristiek, geen transformatie

**Aanpak:**
- Fix `$id` naar `https://juraregel.nl/schemas/jrem/v1.1.0`
- Voeg JSON Schema validatie toe aan CI gate
- Documenteer migratie-regels

### 2.4 Sources/Connectors zijn Non-Functioneel

**Probleem:**
`sources/bwb_connector.py` methoden zijn leeg (`pass` of `...`).

**Aanpak:**
- Implementer minimaal één connector volledig
- Of verwijder stubs en documenteer als "planned"

---

## 3. AI-ETHIEK & ALGORITHME CRITICUS

### 3.1 Geen Transparantie over LLM-Gebruik

**Probleem:**
LLM-gebruik is gedocumenteerd als "met behulp van een LLM", maar welk LLM? Welke prompt? Hoe gevalideerd?

**Wat een AI-ethicus zegt:**
> "Als je LLM-output gebruikt voor juridische regels, moet je dat transparant communiceren. burgers hebben recht te weten hoe besluiten over hen zijn genomen."

**Aanpak:**
- Documenteer per regel: `interpretatieMethode`, `interpretatiePrompt`, `menselijkeReview`

### 3.2 Geen Bias-Detectie

**Probleem:**
Eén persoon + één LLM = één bias.

**Aanpak:**
- Voeg "tweede lezer" proces toe
- Documenteer interpretatie-verschillen

### 3.3 "check_compliance" is Misleading

**Probleem:**
Retourneert `compliance_percentage: 0.0` voor BIO2 — suggereert 0% compliant, wat fout is.

**Aanpak:**
- Hernoem naar `list_measures` of `get_maatregelen`
- Verwijder `compliance_percentage`
- Documenteer beperkingen

---

## 4. PRODUCT & USEABILITY CRITICUS

### 4.1 28 Use Cases — Geen Prioriteit

**Probleem:**
28 use cases, geen enkele productie-ready.

**Wat een productowner zegt:**
> "28 half-producten is slechter dan 3 complete producten."

**Aanpak:**
- Kies top-3 voor productie (griffierecht, toeslagen, publicatie)
- Accordeer met onafhankelijke jurist
- Deprecieer andere 25

### 4.2 Geen Gebruikersdocumentatie

**Probleem:**
Geen "Getting Started", geen "Rule Authoring", geen "Legal Review".

**Aanpak:**
- Schrijf handleidingen voor elke doelgroep

### 4.3 BDD Tests Testen niet de Bron

**Probleem:**
Tests valideren de `match_rule()` functie, niet de JREM exports zelf. Circular reasoning.

**Aanpak:**
- Schrijf tests die JREM exports valideren tegen schema
- Schrijf tests die bronverwijzingen checken
- Schrijf tests die outcomes checken tegen werkelijke wetgeving

---

## 5. GOVERNANCE & BEHEER CRITICUS

### 5.1 Governance Registry is Statisch

**Probleem:**
Registry wordt niet bijgewerkt bij wetswijzigingen.

**Aanpak:**
- Voeg `wettelijkeBasis` en `wijzigingsprocedure` toe
- Koppel harvester aan registry

### 5.2 Geen Versiebeheer voor Regels

**Probleem:**
Geen historiek. Als regel wijzigt, is oude versie verdwenen.

**Aanpak:**
- Git-based versioning
- Voeg `replaces`/`replacedBy` toe
- Bouw "regelhistoriek" endpoint

---

## Conclusie & Prioriteiten

JuraRegel v2.1.0 is een solide technische basis, maar **niet geschikt voor productie** in overheidscontext.

**Top-3 prioriteiten:**

| # | Prioriteit | Impact | Inspanning |
|---|-----------|--------|------------|
| 1 | Juristische accordering | Blokkerend voor productie | 1-2 weken (extern) |
| 2 | Bronverwijzingen | Juridische houdbaarheid | 2-4 weken |
| 3 | Transparantie LLM-gebruik | Ethisch verantwoord | 1 week |

**Daarna:**
- Schema versioning fix ($id bug)
- Connector implementatie
- Gebruikersdocumentatie
- Backup strategy

Zonder deze verbeteringen blijft JuraRegel een demo — geen overheidsplatform.
