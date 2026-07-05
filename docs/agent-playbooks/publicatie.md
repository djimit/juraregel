# Agent Playbook: Pseudonimisering Check

## Wanneer
Gebruik dit playbook om te controleren of uitspraken voldoen aan pseudonimiseringseisen.

## Benodigde informatie
- Type document (uitspraak, conclusie, tussenuitspraak)
- Bevat PII (ja/nee/onbekend)
- Publicatiekanaal (rechtspraak.nl, LIJDAP, andere)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="publicatie"
3. Controleer pseudonimisering status
4. Geef aanbevelingen voor redactie

## Human Escalation
- Bijzondere persoonsgegevens -> rechterlijke macht
- Internationale publicatie -> privacy officer

## Voorbeeld
User: "Is deze uitspraak geschikt voor publicatie op rechtspraak.nl?"
Agent: juraregel.calculate("publicatie", {type:"uitspraak", bevatPII:true, kanaal:"rechtspraak.nl"})
