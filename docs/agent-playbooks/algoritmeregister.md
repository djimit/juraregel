# Agent Playbook: Algoritme-Transparantie

## Wanneer
Gebruik dit playbook om te checken of een algoritme registratieplichtig is.

## Benodigde informatie
- Type algoritme (besluitvorming, risicoscores, aanbevelingen)
- Invloed op burgers (hoog, middel, laag)
- Geautomatiseerde besluitvorming (ja/nee)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="algoritmeregister"
3. Controleer registratieplicht
4. Geef transparantie-eisen

## Human Escalation
- Hoog-risico AI -> AI Act compliance team
- Discriminatievermoeden -> Autoriteit Persoonsgegevens

## Voorbeeld
User: "Moet ons sollicitatie-algoritme in het algoritmeregister?"
Agent: juraregel.calculate("algoritmeregister", {type:"sollicitatie", invloed:"hoog", geautomatiseerd:true})
