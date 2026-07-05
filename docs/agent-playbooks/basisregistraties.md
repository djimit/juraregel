# Agent Playbook: BRP Toegangsbeoordeling

## Wanneer
Gebruik dit playbook om te beoordelen of toegang tot BRP-gegevens rechtmatig is.

## Benodigde informatie
- Doel van toegang (wettelijk doel of niet)
- Type gegevens (basis, uitgebreid, historisch)
- Organisatie (overheid, private partij)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="basisregistraties"
3. Controleer rechtmatigheid
4. Geef voorwaarden voor toegang

## Human Escalation
- Onjuist gebruik -> escalatie naar Autoriteit Persoonsgegevens
- Onbekend doel -> functionaris gegevensbescherming

## Voorbeeld
User: "Mijn gemeente wil BRP-gegevens gebruiken voor handhaving. Mag dat?"
Agent: juraregel.calculate("basisregistraties", {doel:"handhaving", type:"basis"})
