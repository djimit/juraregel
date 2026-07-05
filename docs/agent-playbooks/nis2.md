# Agent Playbook: NIS2 Melding

## Wanneer
Gebruik dit playbook om te beoordelen of een cybersecurity-incident NIS2-meldingsplichtig is.

## Benodigde informatie
- Type incident (ransomware, datalek, DDoS, inbraak)
- Sector (energie, transport, gezondheid, digitale infrastructuur)
- Impact (kritiek, hoog, middel, laag)
- Aantal getroffen gebruikers

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="nis2"
3. Bepaal meldingsplicht (ja/nee, termijn)
4. Geef meldprocedure (CSIRT, CERT, opdrachtgever)

## Human Escalation
- Kritiek incident -> direct NCSC
- Media-aandacht -> communicatie

## Voorbeeld
User: "We hebben een ransomware-aanval. Moeten we dat melden onder NIS2?"
Agent: juraregel.calculate("nis2", {type:"ransomware", sector:"gezondheid", impact:"kritiek"})
