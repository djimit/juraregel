# Classificatie Use Case — Zaaksregistratie

**Als** griffier **wil ik** bij intake een controleerbaar classificatievoorstel krijgen **zodat** uitzonderingen niet automatisch naar de verkeerde zaakstroom gaan.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Handmatige classificatie foutgevoelig | Catalogusregel voor de exacte grens van artikel 93 onder a |
| Burger | Zaak belandt bij verkeerde rechter | Fail-closed voorstel; uitzonderingen blijven handmatig |

3 regels, 3 inhoudelijke tests. Catalog-only op port 8492. L0-demo; geen productieclaim.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | Handmatige zaakclassificatie | Smalle artikel-93-bronmapping voor geldvorderingen |
| Intake medewerker | Foute classificatie → vertraging | Handmatige controle boven de grens en bij bijzondere categorieën |
