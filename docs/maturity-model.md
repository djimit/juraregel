# Rule Maturity Model — Legal RuleOps Platform

## Classificatie van juridische regels op automateerbaarheid

### Level 1: Deterministisch (geen uitzonderingen)
- **Definitie**: Regels die onder alle omstandigheden een vaste uitkomst geven
- **Voorbeeld**: Griffierecht bedrag voor een specifieke tariefcategorie en partijtype
- **In platform**: Ja — volledig geautomatiseerd, geen manualReviewRequired
- **CI gate 14**: Volledige acceptatie vereist

### Level 2: Deterministisch met bekende uitzonderingen
- **Definitie**: Regels met een deterministische hoofdregel en een eindige, bekende set uitzonderingen
- **Voorbeeld**: Griffierecht met verweerStatus=onbekend → manualReviewRequired=true
- **In platform**: Ja — geautomatiseerd met manualReviewRequired flag voor uitzonderingen
- **CI gate 14**: Volledige acceptatie vereist

### Level 3: Deterministisch hoofdregel + discretionaire uitzonderingen
- **Definitie**: Regels met een deterministische hoofdregel maar waarbij uitzonderingen discretionaire beoordeling vereisen
- **Voorbeeld**: Termijnindicator (standaard termijn is deterministisch, maar herstel verzuim is discretionair)
- **In platform**: Ja — als "indicator + manual review". De Rule Service geeft een indicatie, niet een beslissing
- **API response**: Bevat disclaimer "Dit is een indicatie, geen beslissing. De rechter beslist."
- **CI gate 14**: Volledige acceptatie vereist, inclusief discretionaire grenzen

### Level 4: Volledig discretionair
- **Definitie**: Regels die volledig afhangen van rechterlijke oordeelsvorming
- **Voorbeeld**: Vonniswijzing, bewijswaardering, proceskostenveroordeling bijzondere omstandigheden
- **In platform**: Nee — uitgesloten
- **Reden**: De Rule Service stelt voor, de mens beslist. Discretionaire beslissingen zijn geen "voorstellen"

## Toelatingsprocedure

1. **Voorstel**: Nieuwe use case wordt voorgesteld met beschrijving, bronnen, en verwachte regelhardheid
2. **Classificatie**: Toelatingscommissie (juridisch eigenaar + architect) classificeert als L1-L4
3. **Goedkeuring**: L1-L3 → goedgekeurd. L4 → afgewezen.
4. **Rule Extraction Sprint**: Goedgekeurde use cases doorlopen de sprint methodiek

## Acceptatie Differentiatie

| Type | Wanneer | Stappen |
|---|---|---|
| Full acceptatie | Nieuwe use case | 1. Leesbaarheidstest 2. Bronverificatie 3. Scenario-acceptatie 4. Accordering |
| Update acceptatie | Tariefwijziging of reglementupdate | Alleen 3. Scenario-acceptatie + 4. Accordering |

Full acceptatie is vereist voor nieuwe use cases en voor wijzigingen die de regelinterpretatie raken. Update acceptatie is voldoend voor numerieke wijzigingen (tarieven, grenswaarden) die de regelstructuur niet wijzigen.
