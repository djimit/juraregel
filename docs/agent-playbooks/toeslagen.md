# Agent Playbook: Toeslagen Berekenen

## Wanneer
Gebruik dit playbook wanneer een burger vraagt naar recht op zorgtoeslag, huurtoeslag, kinderopvangtoeslag of kindgebonden budget.

## Benodigde informatie
- toeslagType (zorgtoeslag, huurtoeslag, kinderopvangtoeslag, kindgebonden_budget)
- leeftijd
- alleenstaande of samenwonend
- inkomen (jaarinkomen)

## Stappen
1. Valideer input volledigheid
2. Roep juraregel.calculate aan met domain="toeslagen" en de input
3. Controleer outcome.recht: true = rapporteer bedrag, false = rapporteer reden
4. Controleer outcome.manualReviewRequired: true = verwijs naar Toeslagen
5. Geef bronverwijzing mee

## Human Escalation
- manualReviewRequired: true -> verwijs naar Belastingdienst/Toeslagen
- Nationaliteit niet-EU zonder verblijfsrecht -> verwijs naar IND

## Voorbeeld
User: "Ik ben 30, alleenstaand, verdien EUR30.000 per jaar. Heb ik recht op zorgtoeslag?"
Agent: juraregel.calculate("toeslagen", {toeslagType:"zorgtoeslag", leeftijd:30, alleenstaande:true, inkomen:30000})
Resultaat: {recht: true, bedrag: {amount: 123, currency: "EUR", periode: "maandelijks"}}
Antwoord: "Ja, u heeft recht op zorgtoeslag van EUR123 per maand (Toeslagenwet art. 8)."
