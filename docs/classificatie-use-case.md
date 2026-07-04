# Classificatie Use Case — Zaaksregistratie

**Als** griffier **wil ik** bij intake automatisch de juiste zaakstroom bepalen **zodat** de zaak bij de juiste rechter belandt.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Handmatige classificatie foutgevoelig | Rule API classificeert op basis van vorderingwaarde |
| Burger | Zaak belandt bij verkeerde rechter | Deterministische classificatie met uitleg |

3 regels (PoC). Rule API op port 8492. 16 tests. PoC status.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Handmatige zaakclassificatie | Rule API classificeert kanton vs handel |
| Intake medewerker | Foute classificatie → vertraging | Deterministische classificatie met redeneerstappen |
