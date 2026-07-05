# MinBZK Verbeteringen

Dit document beschrijft de verbeteringen op basis van analyse van MinBZK repositories.

## Bronnen

| Repository | URL | Relevantie |
|------------|-----|------------|
| regelrecht | github.com/MinBZK/regelrecht | Versioned schemas, BDD tests, harvester |
| poc-machine-law | github.com/MinBZK/poc-machine-law | MCP resources + prompts |
| NRML | github.com/MinBZK/NRML | Normalized Rule Model Language |
| Algoritmekader | github.com/MinBZK/Algoritmekader | CI validatie scripts |

## Geimplementeerde Verbeteringen

### 1. MCP Resources + Prompts

**Inspiratie:** poc-machine-law heeft naast tools ook resources (`laws://list`) en prompts (`explain_calculation`).

**Implementatie:**
- `mcp-server/juraregel_mcp.py` uitgebrd met `@server.resource()` en `@server.prompt()` handlers
- Resources: `laws://list`, `laws://summary`, `laws://{domain}/spec`, `profile://{domain}`
- Prompts: `check_all_benefits`, `explain_calculation`, `compare_scenarios`
- Test: `mcp-server/test_mcp_resources.py` (9 tests)

**Gebruik door agents:**
```
# Agent kan resources lezen zonder tool call
laws://list -> lijst van alle domeinen
profile://toeslagen -> input/output profiel

# Agent kan prompts gebruiken als pre-built workflows
check_all_benefits(leeftijd=30, inkomen=30000, huishouden=alleenstaande)
```

### 2. JREM Schema Versioning

**Inspiratie:** regelrecht heeft 12 schema versies (v0.0.1 -> v0.5.6) met backwards compatibiliteit.

**Implementatie:**
- `shared/jrem-schema-v1.0.0.json` - basis met `$id: https://juraregel.nl/schemas/jrem/v1.0.0`
- `shared/jrem-schema-v1.1.0.json` - uitbreiding met `governanceLevel`, `bwbId`, `celexId`, `eli`
- `tools/jrem-migrate.py` - automatische migratie tussen versies
- `ci/jrem-schema-version-check.sh` - CI gate

**Nieuwe velden in v1.1.0:**
```json
{
  "governanceLevel": "rijk",
  "bwbId": "BWBR0005291",
  "celexId": "32024R1689",
  "eli": "http://data.europa.eu/eli/reg/2024/1689"
}
```

### 3. Gherkin BDD Tests

**Inspiratie:** regelrecht gebruikt Gherkin scenarios die door juristen leesbaar zijn.

**Implementatie:**
- `features/*.feature` - 3 feature files, 7 scenarios
- `features/steps/juraregel_steps.py` - step definitions met `match_rule()` logica
- `features/conftest.py` - gedeelde `ctx` fixture
- `ci/run-bdd-tests.sh` - CI gate

**Voorbeeld:**
```gherkin
Feature: Zorgtoeslag calculation
  Scenario: Single person with income below threshold is entitled
    Given the domain "toeslagen" is loaded
    And a single person of 30 years old
    And an annual income of 30000 euros
    When I calculate the healthcare benefit
    Then the entitlement is "true"
    And the amount is 123 euros per month
```

### 4. BWB Harvester

**Inspiratie:** regelrecht heeft een geautomatiseerde harvester die BWB periodiek scant.

**Implementatie:**
- `sources/harvester.py` - BWB API client met diff detection
- State tracking in `.data/harvester-state.json`
- `python3 sources/harvester.py --health` - health check
- `python3 sources/harvester.py --check` - check voor updates
- `ci/harvester-health.sh` - CI gate

**Gebruik:**
```bash
# Health check
python3 sources/harvester.py --health

# Check voor nieuwe/gewijzigde wetten
python3 sources/harvester.py --check

# Bekijk harvester state
python3 sources/harvester.py --state
```

## Toekomstige Verbeteringen (nog niet geimplementeerd)

### Van regelrecht:
- **Polyglot engine** - Rust voor performance, Python voor flexibiliteit
- **Web editor** - Vue 3 UI voor regel editing met live preview
- **PostgreSQL job queue** - voor grootschaalse verwerking
- **Mutation testing** - test kwaliteit meten

### Van NRML:
- **NRML compatibiliteit** - bridge format tussen JREM en RegelSpraak
- **Multilingual core** - NL/EN in kern structuur
- **XSLT transformaties** - JREM -> RegelSpraak

### Van Algoritmekader:
- **Container deployment** - non-root nginx image
- **URN uniqueness validation** - CI gate
