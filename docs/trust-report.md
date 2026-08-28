# JuraRegel Trust Report

**Datum:** 2026-08-28

**Repo:** `djimit/juraregel`

**Snapshot:** merge `4e3de85`
**Status:** technisch PoC-ready; niet productie-ready zonder onafhankelijke
juridische validatie en geldige acceptatie-evidence.

## Executive Readiness

De huidige repository bevat 58 JREM-exports met samen 1.258 regels. De gates
behandelen 50 exports als `L0-demo` en 8 als `L1-poc`; 22 van de L0-exports
missen nog een expliciet `maturityLevel`. Er zijn geen `L2-pilot`- of
`L3-production`-claims.

Vijf domeinen hebben een bewezen `calculate`-pad: `griffierecht`, `toeslagen`,
`omgevingswet`, `basisregistraties` en `participatiewet`. Alle andere exports
zijn catalogi en mogen geen geautomatiseerd juridisch oordeel geven.

## Repository Evidence

| Check | Status | Evidence |
|---|---:|---|
| Volledige lokale gate | pass | `bash ci/run-all-gates.sh`: 561 tests en alle overige gates groen |
| JKB-consistentie | pass | `python3 tools/jkb-builder.py --check-only`: 1.258 bronregels en 1.258 indexregels; geen ontbrekende, extra of incomplete entries |
| Source quality | debt/pass | `python3 ci/source_quality.py`: 282 bekende schulditems, 0 blocking en 0 regressions |
| L2-promotion preflight | guard/pass | 7 kandidaten gecontroleerd; 0 ready en 0 blocking omdat geen export L2/L3 claimt |

Dit is repository- en gate-evidence. Het bewijst geen actuele werking van
optionele vectorstores, externe bronendpoints of onafhankelijke juridische
juistheid.

### Niet-blokkerende gatesignalen

- JREM-validatie: 112 waarschuwingen en 0 fouten, vooral ontbrekende
  approval-objecten en identifiers in oudere exports.
- Legal-review gate: 35 self-approvalwaarschuwingen en 0 blokkades.
- Pytest: 15 deprecation-waarschuwingen uit `Starlette`/`pytest-bdd`-
  afhankelijkheden.
- JKB vector- en keywordcoverage zijn overgeslagen omdat de optionele lokale
  stores niet aanwezig waren; de JSON-indexconsistentie is wel bewezen.

## Source-quality Debt

Alle 282 bekende items zitten in 17 L0-exports en zijn daardoor niet
blokkerend. De baseline voorkomt groei; zij maakt bestaande schuld niet
acceptabel.

| Type | Aantal |
|---|---:|
| `section` is geen exacte juridische vindplaats | 277 |
| URL ontbreekt | 2 |
| Bronversie of brondatum ontbreekt | 2 |
| BWB-, CELEX- of ELI-identificatie ontbreekt | 1 |

Voor L2/L3 zijn exacte, reproduceerbare bronankers verplicht. Nieuwe schuld of
schuld in een L2/L3-export laat de gate falen.

## Rechtspraak Trust Reset

| Domein | Huidige status | Grens |
|---|---|---|
| `classificatie` | 3 L0-catalogusregels met 3 scenario's | Smalle mapping van artikel 93 onder a Rv; geen uitvoerbaar classificatiebesluit |
| `procesreglement` | 20 historische placeholders plus 1 quarantaine-invariant | Alle uitkomsten zijn `insufficient_evidence` en vereisen handmatige controle; geldig tot en met 2026-06-30 |
| `basisregistraties` | 2 onbewezen kennisvereisten verwijderd | Geen resterende source-quality schuld in deze export |

Voor `procesreglement` moet de bronextractie per geldigheidsperiode opnieuw
worden opgebouwd uit de officiële reglementen 2025/2026 en de opvolgende
bronnen vanaf juli 2026. Zie
[`procesreglement-use-case.md`](procesreglement-use-case.md) en
[`classificatie-use-case.md`](classificatie-use-case.md).

## L2 Acceptance Status

De promotion preflight controleert zeven kandidaten. Geen is gereed:

- `decentrale-regelcheck`, `woo-publicatieplicht-preflight` en `sttr-preflight`
  missen ingevulde, geaccepteerde reviewtemplates;
- `procesreglement` heeft daarnaast 20 bronkwaliteitsissues;
- `classificatie` mist onafhankelijke scenarioacceptatie;
- `eu-ai-act` en `avg-gdpr` bevatten elk 25 deterministische regels zonder
  uitvoerbare voorwaarden, betekenisvolle uitkomst of handmatige controle.

Voor `L2-*` en `L3-*` vereist de gate onafhankelijke approval, volledige en
geldige juristaccordering, een passende bron-snapshot, geaccepteerde scenario's
en semantisch uitvoerbare regels. `L3-*` vereist daarnaast de
indicator-disclaimer en `manualReviewBoundary=indicator-only`.

## Human Gates Remaining

1. Los de 282 bronkwaliteitsitems op met exacte, versieerbare vindplaatsen.
2. Herbouw en beoordeel het procesreglement per geldigheidsperiode.
3. Laat scenario's en juridische interpretaties onafhankelijk accepteren voor
   ieder domein dat naar L2 moet.
4. Herstel de semantische uitvoerbaarheid van `eu-ai-act` en `avg-gdpr` voordat
   promotie wordt overwogen.
5. Beoordeel integratie-evidence uit OpenMythos en Djimitflo afzonderlijk; die
   systemen vervangen de JuraRegel-promotiegates niet.

## Residual Risk

- L0/L1 betekent geen productiegeschiktheid of juridisch advies.
- Catalogusdekking bewijst niet dat een regel uitvoerbaar, actueel of volledig
  juridisch gevalideerd is.
- De optionele semantische zoeklaag en externe harvesters vereisen afzonderlijke
  live verificatie; de lokale JKB-check bewijst alleen indexconsistentie.
- De source-quality baseline is een regressiegrens, geen kwaliteitskeurmerk.
