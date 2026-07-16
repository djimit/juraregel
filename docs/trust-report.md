# JuraRegel Trust Report

**Datum:** 2026-07-16
**Repo:** `djimit/juraregel`
**Change:** `judicial-ai-assurance` 2026.1
**Status:** technisch PoC-ready; niet productie-ready zonder eindgates.

## Executive Readiness

JuraRegel heeft 702 JKB-regels over 31 logische domeinen. De huidige JREM exports hebben 26 `L0-demo` en 8 `L1-poc` rulesets. Er zijn geen `L2-pilot` of `L3-production` claims.

De nieuwe live bronlaag is read-only en gebruikt alleen openbare metadata/search-pagina's. De bronlaag ondersteunt preflight-signalen, geen finale juridische besluiten.

## CI Evidence

| Check | Status | Evidence |
|---|---:|---|
| Laatste GitHub Actions run | pass | run `28829466813`, commit `cfa1753`, conclusion `success` |
| Huidige lokale repositorygate | pass | `bash ci/run-all-gates.sh`: 286 tests, 29 OpenAPI-schema's en SDK-typecheck groen |
| JKB coverage | generated | `python3 tools/jkb-builder.py`: 702 regels, 31 JREM-domeinnamen |
| Source health | pass/deprecated | BWB, EUR-Lex, Rechtspraak, UPL, TOOI/ROO, CVDR/SRU, Woo-index/DiWoo en STTR/IMTR+RTR `ok`; PLOOI bewust `deprecated` |
| Live harvester smoke | pass | CVDR 3 resultaten; Woo-index 5 organisaties; STTR ondersteund `3.0`, `2.0`, `1.5` |
| Jurist gate policy | pass as policy | L2/L3 faalt zonder uitgebreide juristAccordering; L3 vereist indicator-disclaimer en `indicator-only` boundary |
| L2 promotion preflight | pass as guard | 3 target packages checked; 0 ready, 0 blocking; placeholders houden L2-promotie tegen |

## Live Harvester Status

| Bron | Live pad | Status | Grenzen |
|---|---|---:|---|
| CVDR/SRU | `https://lokaleregelgeving.overheid.nl/ZoekResultaat` met `locatie`, `tekst`, `count` | ok | Normaliseert zoekresultaten en sourceRefs; haalt geen volledige regelingsteksten in bulk op |
| Woo-index/DiWoo | `https://organisaties.overheid.nl/woo/zoeken` en organisatiepagina's | ok | Leest publicatielocaties/categorieen; haalt geen documentbody's of private inhoud op |
| STTR/IMTR+RTR | `https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/` | ok | Leest ondersteunde versies en lokale package-metadata; geen DSO/RTR submission-client |

## Maturity And Acceptance

| Domein | Maturity | Acceptance | Readiness |
|---|---:|---:|---|
| `decentrale-regelcheck` | L1-poc | draft/self | Live CVDR metadata-preflight; productiepromotie geblokkeerd tot juristacceptatie |
| `woo-publicatieplicht-preflight` | L1-poc | draft/self | Live Woo publicatielocatie-preflight; metadata-only, geen documentinhoud |
| `sttr-preflight` | L1-poc | draft/self | Live STTR versie-discovery en package metadata checks; geen formele DSO-validatie |
| `judicial-ai-assurance` | L1-poc | draft/self | Catalog-only; 12 controls en 9 niet-compenseerbare hard stops; juridische en governance-review open |
| Overige JREM exports | L0-demo/L1-poc | self of draft/full metadata | Geen L2/L3 readiness claim |

## L2 Acceptance Package Status

| Domein | Package status | Reviewer metadata | Source snapshot | Scenario acceptance | Claim |
|---|---:|---:|---:|---:|---|
| `decentrale-regelcheck` | template-ready | placeholder | placeholder dates | placeholder decisions | Geen L2 claim; blijft `L1-poc` |
| `woo-publicatieplicht-preflight` | template-ready | placeholder | placeholder dates | placeholder decisions | Geen L2 claim; blijft `L1-poc` |
| `sttr-preflight` | template-ready | placeholder | placeholder dates | placeholder decisions | Geen L2 claim; blijft `L1-poc` |

De acceptance templates staan in `docs/acceptance-templates/`. Ze zijn machineleesbaar en human-fillable, maar niet juridisch geaccepteerd zolang placeholders aanwezig zijn. `ci/l2_promotion_preflight.py` rapporteert daarom `ready=false` voor alle drie domeinen en blokkeert alleen als een JREM export al naar `L2-*` of `L3-*` is gezet zonder geldige metadata.

## L2/L3 Gate Contract

Voor `L2-*` en `L3-*` vereist de gate:

- `approval.type` is niet `self`.
- `metadata.acceptatieType` is `full` of `update`.
- `metadata.juristAccordering` bevat `geaccondeerdDoor`, `rol`, `organisatie`, `datum`, `geldigTot`, `versie`, `scope`, `bronSnapshot`, `verklaring` en niet-lege `beperkingen`.
- `juristAccordering.versie` is gelijk aan JREM `version`.
- `geldigTot` is niet verlopen.
- `L3-*` bevat `metadata.indicatorDisclaimer` en `metadata.manualReviewBoundary=indicator-only`.

## Human Gates Remaining

1. Laat de broninterpretatie en hard-stopformuleringen onafhankelijk juridisch beoordelen.
2. Laat de rechterlijke-governancegrens voor autonomie, menselijke toegang en equality of arms beoordelen.
3. Keur een eventuele evidence-integratie met OpenMythos en Djimitflo afzonderlijk goed.
4. Lever jurist-acceptatie metadata per domein dat naar L2/L3 moet en keur die maturity-wijziging expliciet goed.

## Residual Risk

- CVDR en Woo zijn HTML-search gebaseerde publieke contracten; bij markupwijziging degraderen de live-smokes in plaats van stil verkeerde data te leveren.
- Woo `tooiCode` en `publishedAt` zijn niet altijd beschikbaar op de publieke Woo-index detailpagina; ontbrekende metadata blijft manual review.
- STTR package checks zijn metadata-preflights; volledige XSD/verificatiematrix/DSO-submission blijft buiten scope.
- Er is nog geen onafhankelijke juridische acceptatie voor de drie L1-preflightdomeinen of het nieuwe `judicial-ai-assurance`-profiel.
