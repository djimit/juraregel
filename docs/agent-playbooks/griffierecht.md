# Agent Playbook: Griffierecht Berekenen

## Wanneer
Gebruik dit playbook om griffierecht te berekenen voor een procedure bij de rechtspraak.

## Benodigde informatie
- Type procedure (civiel, bestuurlijk, cassatie)
- Type partij (natuurlijk persoon, rechtspersoon, overheid)
- Bedrag in geschil (optioneel)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="griffierecht"
3. Controleer outcome.griffierecht (bedrag)
4. Geef wettelijke bron

## Human Escalation
- Complexe geschillen -> Griffie
- Vrijstelling aanvragen -> rechter

## Voorbeeld
User: "Hoeveel griffierecht betaal ik voor een eis van EUR5.000?"
Agent: juraregel.calculate("griffierecht", {type:"civiel", partij:"natuurlijk_persoon", bedrag:5000})
