# Agent Playbook: NORA Architectuur-Check

## Wanneer
Gebruik dit playbook om een IT-project te toetsen tegen NORA architectuurprincipes.

## Benodigde informatie
- Type project (nieuwe dienst, migratie, integratie)
- Betrokken partijen (gemeente, provincie, rijk, waterschap)
- Data-deling (ja/nee)

## Stappen
1. Valideer input
2. Roep juraregel.get_governance aan met domain="nora"
3. Check NORA-principes (hergebruik, open standaarden, privacy by design)
4. Geef architectuur-aanbevelingen

## Human Escalation
- Afwijking van NORA -> enterprise architect
- Cross-gemeentelijke afstemming -> VNG/King

## Voorbeeld
User: "Voldoet onze nieuwe burgerportal aan NORA?"
Agent: juraregel.get_governance("nora") + architectuur-check
