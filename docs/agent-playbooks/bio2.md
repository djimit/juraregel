# Agent Playbook: BIO2 Compliance Audit

## Wanneer
Gebruik dit playbook voor een informatiebeveiligingsaudit tegen BIO2/ENSIA baseline.

## Benodigde informatie
- Organisatietype (ministerie, provincie, gemeente, zorg, onderwijs)
- Huidige maatregelen (lijst van geimplementeerde maatregelen)

## Stappen
1. Roep juraregel.check_compliance aan met domain="bio2"
2. Analyseer gaps (regels met status unknown of manual_review_required)
3. Prioriteer gaps op basis van risico
4. Genereer actieplan

## Human Escalation
- Gaps met hoog risico -> escalatie naar CISO
- Budgettaire beslissingen -> management

## Voorbeeld
User: "Wat ontbreekt er in onze BIO2 implementatie?"
Agent: juraregel.check_compliance("bio2") -> gaps analyse -> prioriteiten
