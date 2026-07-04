# Rule Extraction Sprint — Methodiek

## Doel
Een gestructureerde methode om juridische regels van bron (wet/regeling/PDF) naar geteste, geaccepteerde Rule Service te transformeren.

## Sprint Duur
- Simpel (≤20 regels): 1-2 weken
- Middel (20-40 regels): 2-3 weken
- Complex (40+ regels): 3-4 weken
Plus wachttijd op jurist-acceptatie (1-2 weken)

## Dag-voor-Dag Methodiek

### Dag 1: Bronverzameling
- Verzamel alle relevante bronnen (wet, regeling, tarieftabel, procesreglement)
- Identificeer alle regels, uitzonderingen en boundary cases
- Documenteer onduidelijkheden voor jurist-review
- Output: bronnenlijst met BWBR-identifiers

### Dag 2: Begrippenmodel
- Definieer alle begrippen in begrippen.rspraak
- Valideer met jurist: zijn de definities correct?
- Output: begrippen.rspraak met ≥5 begrippen

### Dag 3-4: Beslistabellen
- Schrijf regels in regels-YYYY.rspraak
- Schrijf verweer/uitzonderingslogica
- Boundary operatoren (>=, <) gedocumenteerd met wettekst-referentie
- Output: regels-YYYY.rspraak met ≥10 regels

### Dag 5: JREM Export + Tests
- Vertaal RegelSpraak naar JREM export
- Schrijf test scenario's (happy path + boundary + negative)
- Run CI gates (1-13, gate 14 SKIP voor draft)
- Output: JREM export + test suite

### Dag 6-7: Jurist-Acceptatie
- Jurist leest RegelSpraak zonder code-uitleg (leesbaarheidstest)
- Jurist verifieert bronverwijzingen (bronverificatie)
- Jurist accordeert scenarios (scenario-acceptatie)
- Jurist ondertekent accordering (naam, datum, geldigTot, versie)
- Output: getekende accordering

## Jurist-Acceptatie Protocol

### Stap 1: Leesbaarheidstest
- Jurist krijgt 10 willekeurige regels
- Zonder code-uitleg, zonder hulp
- Vraag per regel: "Wat betekent deze regel?"
- Score: 0 kritieke fouten + ≤1 serieus + ≤2 minor = PASS

### Stap 2: Bronverificatie
- Jurist krijgt alle sourceRefs uit de JREM
- Vraag: "Is dit de juiste bron? Is de section-verwijzing correct?"
- Score: 100% correct = PASS

### Stap 3: Scenario-acceptatie
- Jurist krijgt 10 scenarios (input + expected output)
- Vraag: "Is deze verwachte uitkomst juridisch correct?"
- Score: ≥95% correct = PASS

### Stap 4: Accordering
- Jurist ondertekent: "Deze regelset is juridisch accoord"
- Accordering opgeslagen met naam, functie, datum, versie
- Geldigheid: 1 jaar, daarna her-accordering vereist

## Templates

### Begrippen template
```
begrip <naam>: "<beschrijving>" waarden: <waarde1>, <waarde2>.
```

### Regel template
```
regel <id> "<naam>":
  als <voorwaarde1>
  en <voorwaarde2>
  dan is <resultaat1>
  en is <resultaat2>.
```

### JREM metadata template
```json
{
  "metadata": {
    "juridischeContext": {
      "wet": "<wetnaam>",
      "wetBwbrId": "BWBR<id>",
      "wetVersieLaatstGecheckt": "<datum>",
      "tariefVersie": "<versie>"
    },
    "juristAccordering": {
      "geaccondeerdDoor": "<naam>",
      "datum": "<datum>",
      "geldigTot": "<datum+1jaar>",
      "versie": "<JREM versie>"
    },
    "acceptatieType": "full"
  }
}
```
