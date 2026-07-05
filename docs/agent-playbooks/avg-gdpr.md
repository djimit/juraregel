# Agent Playbook: AVG Verwerkingsgrond Check

## Wanneer
Gebruik dit playbook om te beoordelen of een gegevensverwerking een geldige rechtsgrond heeft onder AVG/GDPR.

## Benodigde informatie
- Type verwerking (opslag, delen, profilering, besluitvorming)
- Gegevenscategorie (gewoon, bijzonder, strafrechtelijk)
- Rechtsgrond (toestemming, contract, wettelijke plicht, gerechtvaardigd belang)
- Betrokkenen (klanten, werknemers, burgers, kinderen)

## Stappen
1. Valideer input
2. Roep juraregel.calculate aan met domain="avg-gdpr"
3. Controleer rechtsgeldigheid
4. Geef aanbevelingen voor documentatie

## Human Escalation
- Bijzondere categorieen -> functionaris gegevensbescherming
- Grensoverschrijdende verwerking -> Lead Supervisory Authority
- Kinderen (<16) -> toestemming ouders vereist

## Voorbeeld
User: "Mogen we e-mailadressen van klanten gebruiken voor marketing?"
Agent: juraregel.calculate("avg-gdpr", {type:"marketing", gegevenscategorie:"gewoon", rechtsgrond:"toestemming"})
