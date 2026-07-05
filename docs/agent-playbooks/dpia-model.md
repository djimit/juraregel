# Agent Playbook: DPIA Beoordeling

## Wanneer
Gebruik dit playbook om te beoordelen of een DPIA (Data Protection Impact Assessment) verplicht is.

## Benodigde informatie
- Type verwerking
- Gegevenscategorie (gewoon, bijzonder, strafrechtelijk)
- Aantal betrokkenen
- Systematische monitoring (ja/nee)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="dpia-model"
3. Controleer DPIA-plicht (ja/nee)
4. Geef aanbevelingen voor mitigerende maatregelen

## Human Escalation
- Hoog risico zonder mitigerende maatregelen -> AP voorafgaand overleg
- Twijfelgevallen -> functionaris gegevensbescherming

## Voorbeeld
User: "Moeten we een DPIA doen voor ons nieuwe klantprofileringssysteem?"
Agent: juraregel.calculate("dpia-model", {type:"profilering", gegevenscategorie:"gewoon", monitoring:true})
