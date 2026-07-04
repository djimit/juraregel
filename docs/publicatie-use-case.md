# Publicatie/PII Use Case — Pseudonimiseringsrichtlijn Engine

**Als** griffier **wil ik** bij publicatie automatisch persoonsgegevens classificeren **zodat** de pseudonimiseringsrichtlijn correct wordt toegepast.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | PII handmatig classificeren — foutgevoelig | V4.2 engine classificeert automatisch (100% op 25K) |
| Burger | PII niet correct gepseudonimiseerd | Engine respecteert richtlijn-uitzonderingen |
| Privacy officer | Geen controle op pseudonimisering | Audit trail met classificatie per detectie |

3 regels + V4.2 pseudonimiseringsrichtlijn engine (100% precision op 25.127 uitspraken). Rule API op port 8493. 31 tests. Production status.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | PII classificeren handmatig | V4.2 engine classificeert automatisch |
| Privacy officer | PII lekken in publicaties | Engine herkent false positives (professionals/overheid) |
| Auditor | Geen trail van pseudonimiseringsbeslissingen | Audit trail met calculationId + hashes |
| Data scientist | Wil PII-scan integreren | Engine als Python module importeerbaar |
