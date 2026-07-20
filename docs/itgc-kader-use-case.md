# ADR ITGC-kader v1.1 in JuraRegel

## Besluit

Het ITGC-kader is opgenomen als **L1-PoC, catalog-only**. JuraRegel bewaart de
officiële ADR ZIP, verifieert de bronhash, extraheert de XLSX deterministisch en
publiceert 48 beheersmaatregelen met 147 toetsingscriteria. De API berekent geen
compliance en retourneert zonder organisatiebewijs `insufficient_evidence`.

Het kader is bruikbaar als auditprofiel en evidence-checklist, niet als volledige
BIO2-vervangingsset of juridische norm. ADR positioneert het als een selectie voor
de jaarrekeningcontrole, laat professioneel oordeel bij de gebruiker en sluit het
ontlenen van rechten uit.

## Bronwaarheid

| Onderdeel | Vastgesteld |
|---|---:|
| Beheersdoelstellingen | 8 (R1, R2, A1, G1, W1, I1, C1, S1) |
| Basismaatregelen | 48 |
| Toetsingscriteria | 147 |
| Toetsingstypen | Opzet; Bestaan/Werking |
| Lokale bron | `sources/adr-itgc-kader-v1-1.zip` |
| Bronintegriteit | SHA-256 voor ZIP, XLSX en PDF vastgelegd |

De versiehistorie vermeldt voor v1.1 van 12 mei 2026: referentieteksten zijn
verwijderd. Leveranciersmanagement (L1) ontbreekt expliciet en was voor later in
2026 aangekondigd. De publicatiepagina noemt 54 PDF-pagina's, terwijl het
officiële gedownloade PDF-bestand technisch 37 pagina's bevat; dit is als
metadata-afwijking geregistreerd en verandert de XLSX-extractie niet.

## API en regeneratie

```bash
.venv/bin/python use-cases/itgc-kader/lib/itgc_parser.py \
  use-cases/itgc-kader/sources/adr-itgc-kader-v1-1.zip \
  use-cases/itgc-kader/jrem/exports/itgc-kader-2026.1.json
python3 use-cases/itgc-kader/api/app.py
curl 'http://127.0.0.1:8522/v1/itgc-kader/maatregelen?doelstelling=A1'
```

`POST /v1/itgc-kader/calculate` geeft bewust `409 catalog_only`. Een latere
evidence-laag moet per toetsingscriterium bron, periode, scope, actor, hash,
verkrijgingswijze en reviewerbesluit vastleggen. Tot die laag onafhankelijk is
beoordeeld, mag geen totaalscore of auditconclusie worden afgeleid.

## Djimitflo, LongCat 2.0 en OpenMythos

Op 16 juli 2026 zijn via Djimitflo twaalf afzonderlijke inhoudelijke runs met
`longcat/LongCat-2.0` uitgevoerd, plus tien afzonderlijke OpenMythos-cases. Tien
inhoudelijke runs leverden substantieel antwoord; twee liepen tegen
toolpermissies aan. Meerdere vrije analyses verzonnen aantallen, werkbladkolommen
of controlfamilies. Zij zijn daarom alleen als kritiek en ontwerpinput gebruikt;
de catalogus komt uitsluitend uit de mechanische XLSX-extractie.

De tien OpenMythos-cases gaven volgens de strikte oracle 3/10 pass. Handmatige
adjudicatie maakt één Nederlandstalige weigering tot een regex-false-negative,
maar laat ernstige fouten over: canary-lekkage, een ongefundeerde DOI en
hallucinatie rond een fictieve zaak. Twee runs eindigden zonder eindantwoord.
Daarom geldt LongCat hier niet als autonome bron of beoordelaar. Toelaatbaar is:
samenvatten, hypothesen formuleren en review ondersteunen na bronextractie;
ontoelaatbaar is: controls creëren, bewijs vaststellen of compliance concluderen.

## Promotiegrens

L2 vereist minimaal een onafhankelijke auditorreview van de mapping, een
geschematiseerd evidence-bundle, negatieve tests voor ontbrekend of conflicterend
bewijs, en bewijs dat de 147 criteria reproduceerbaar aan bronpassages zijn
gekoppeld. L3 vereist daarnaast aantoonbare werking in een echte auditcyclus,
functiescheiding, immutable audit trail, herbeoordeling bij bronversiewijziging en
een expliciet besluit over het ontbrekende leveranciersmanagement.
