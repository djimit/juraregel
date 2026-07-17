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

## NEDERUS Koppeling

NIS2 is één van de vier frameworks in het [NEDERUS](../../openspec/changes/nederus-framework-v1/sources/README.md) framework. NED-01 (AI Impact Assessment) en NED-05 (Incident Response) mappen naar NIS2:

| NEDERUS Control | NIS2 Mapping | Conflict |
|---|---|---|
| NED-01 AI Impact Assessment | Art. 21: Risk management | — |
| NED-05 Incident Response | Art. 23: Incident reporting (24h) | EU AI Act Art. 72 allows 15d — apply most stringent (24h) |

Zie [NEDERUS conflicts](../../openspec/changes/nederus-framework-v1/sources/crosswalks/conflicts.md) voor timing-conflict resolutie.

## Voorbeeld
User: "We hebben een ransomware-aanval. Moeten we dat melden onder NIS2?"
Agent: juraregel.calculate("nis2", {type:"ransomware", sector:"gezondheid", impact:"kritiek"})
