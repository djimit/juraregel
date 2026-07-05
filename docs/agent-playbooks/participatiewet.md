# Agent Playbook: Bijstandsrechten Bepalen

## Wanneer
Gebruik dit playbook wanneer een burger vraagt naar recht op bijstand.

## Benodigde informatie
- leeftijd
- alleenstaande of samenwonend
- inkomen
- vermogen
- woonplaats (gemeente)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="participatiewet"
3. Controleer outcome.bijstand (ja/nee)
4. Controleer vermogensgrens
5. Geef verwijzing naar gemeente indien van toepassing

## Human Escalation
- Institutionele woonsituatie -> verwijs naar gemeente
- Bezwaar procedure -> juridisch adviseur

## Voorbeeld
User: "Heb ik recht op bijstand? Ik ben 25, alleenstaand, geen inkomen."
Agent: juraregel.calculate("participatiewet", {leeftijd:25, alleenstaande:true, inkomen:0})
