# JuraRegel Trust Report

**Datum:** 2026-07-07
**Repo:** `djimit/juraregel`
**Head:** `55ebadf`
**Status:** technisch PoC-ready; niet productie-ready zonder eindgates.

## Executive Readiness

JuraRegel heeft 690 JKB-regels over 30 domeinen. De huidige JREM exports hebben 26 `L0-demo` en 7 `L1-poc` rulesets. Er zijn geen `L2-pilot` of `L3-production` claims.

De nieuwe live bronlaag is read-only en gebruikt alleen openbare metadata/search-pagina's. De bronlaag ondersteunt preflight-signalen, geen finale juridische besluiten.

## CI Evidence

| Check | Status | Evidence |
|---|---:|---|
| Laatste GitHub Actions run | pass | run `28827497816`, commit `55ebadf`, conclusion `success` |
| JKB coverage | pass | `knowledge-base/jkb-summary.json`: 690 regels, 30 domeinen |
| Source health | pass/deprecated | BWB, EUR-Lex, Rechtspraak, UPL, TOOI/ROO, CVDR/SRU, Woo-index/DiWoo en STTR/IMTR+RTR `ok`; PLOOI bewust `deprecated` |
| Live harvester smoke | pass | CVDR 3 resultaten; Woo-index 5 organisaties; STTR ondersteund `3.0`, `2.0`, `1.5` |
| Jurist gate policy | pass as policy | L2/L3 faalt zonder uitgebreide juristAccordering; L3 vereist indicator-disclaimer en `indicator-only` boundary |

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
| Overige JREM exports | L0-demo/L1-poc | self of draft/full metadata | Geen L2/L3 readiness claim |

## L2/L3 Gate Contract

Voor `L2-*` en `L3-*` vereist de gate:

- `approval.type` is niet `self`.
- `metadata.acceptatieType` is `full` of `update`.
- `metadata.juristAccordering` bevat `geaccondeerdDoor`, `rol`, `organisatie`, `datum`, `geldigTot`, `versie`, `scope`, `bronSnapshot`, `verklaring` en niet-lege `beperkingen`.
- `juristAccordering.versie` is gelijk aan JREM `version`.
- `geldigTot` is niet verlopen.
- `L3-*` bevat `metadata.indicatorDisclaimer` en `metadata.manualReviewBoundary=indicator-only`.

## Human Gates Remaining

1. Bevestig of openbare endpoints volstaan of dat geauthenticeerde endpoints gebruikt mogen worden.
2. Geef publicatie-approval voor dit trust report en source reports.
3. Lever jurist-acceptatie metadata per domein dat naar L2/L3 moet.
4. Keur eventuele L2/L3 maturity-wijzigingen expliciet goed.
5. Keur commit en push goed.

## Residual Risk

- CVDR en Woo zijn HTML-search gebaseerde publieke contracten; bij markupwijziging degraderen de live-smokes in plaats van stil verkeerde data te leveren.
- Woo `tooiCode` en `publishedAt` zijn niet altijd beschikbaar op de publieke Woo-index detailpagina; ontbrekende metadata blijft manual review.
- STTR package checks zijn metadata-preflights; volledige XSD/verificatiematrix/DSO-submission blijft buiten scope.
- Er is nog geen onafhankelijke juridische acceptatie voor de drie nieuwe L1-preflightdomeinen.
