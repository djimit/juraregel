# Agent Playbook: Vergunningplicht Checken

## Wanneer
Gebruik dit playbook wanneer iemand vraagt of een activiteit vergunningplichtig is onder de Omgevingswet.

## Benodigde informatie
- activiteit (bouwen, slopen, verbouwen, kappen, etc.)
- locatie (gemeente, provincie, waterschap)
- omvang (optioneel)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="omgevingswet"
3. Controleer outcome.vergunningplichtig
4. Geef gemeentelijke verwijzing indien van toepassing

## Human Escalation
- Locatie-specifieke regels -> verwijs naar gemeente
- Provinciaal beleid -> verwijs naar provincie

## Voorbeeld
User: "Mag ik een bijouw bouwen in Amsterdam?"
Agent: juraregel.calculate("omgevingswet", {activiteit:"bouwen", locatie:"Amsterdam"})
