# EU AI Act Use Case — AI-systeem Compliance

**Als** AI-developer of compliance officer **wil ik** automatisch valideren of mijn AI-systeem voldoet aan de EU AI Act **zodat** ik niet handmatig 12 artikelen hoef te checken.

| Rol | Probleem | Oplossing |
|---|---|---|
| AI developer | Onbekend welke AI Act verplichtingen van toepassing zijn | Rule API classificeert: verboden/hoog/beperkt/minimaal risico |
| Compliance officer | Conformity assessment vereisten onduidelijk | Check art. 9-12 + 43 regels |
| Bestuurder | Fundamentele rechten impact onbekend | Check art. 27 vereisten |

12 regels: classificatie (4), conformity (4), transparantie (2), rechten (1). Rule API op port 8498.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| AI developer | Onbekend welke verplichtingen van toepassing zijn | Rule API classificeert: verboden/hoog/beperkt/minimaal |
| Compliance officer | Conformity assessment onduidelijk | Check art. 9-12 + 43 regels |
| Bestuurder | Fundamentele rechten impact onbekend | Check art. 27 vereisten |

## NEDERUS Koppeling

De EU AI Act is primair wettelijk kader in het [NEDERUS](../openspec/changes/nederus-framework-v1/sources/README.md) framework. Alle 5 NEDERUS controls dekken EU AI Act artikelen:

| NEDERUS Control | EU AI Act Articles | JuraRegel Implementatie |
|---|---|---|
| NED-01 AI Impact Assessment | Art. 9(2), Art. 27 (FRIA) | `POST /v1/eu-ai-act/classify` |
| NED-02 Bias & Fairness Testing | Art. 10 (Data governance) | Via JREM regels |
| NED-03 Human Oversight | Art. 14 | Via JREM regels |
| NED-04 Transparency | Art. 13, Art. 50 | Via JREM regels |
| NED-05 Incident Response | Art. 72 | Via JREM regels |

Zie de [NEDERUS crosswalk voor EU AI Act](../openspec/changes/nederus-framework-v1/sources/crosswalks/eu-ai-act.md) voor artikel-niveau mapping.

