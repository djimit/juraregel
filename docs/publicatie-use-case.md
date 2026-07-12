# Publicatie/PII Use Case — Pseudonimiseringsrichtlijn Engine

> **Status: catalogus/onderzoeksprototype.** De classificatie-uitkomsten zijn
> niet op een onafhankelijke gold set gevalideerd en mogen niet als productie- of
> 100%-nauwkeurigheidsclaim worden gebruikt.

**Als** griffier **wil ik** bij publicatie automatisch persoonsgegevens classificeren **zodat** de pseudonimiseringsrichtlijn correct wordt toegepast.

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | PII handmatig classificeren — foutgevoelig | V4-engine geeft een reproduceerbaar classificatievoorstel voor menselijke controle |
| Burger | PII niet correct gepseudonimiseerd | Engine respecteert richtlijn-uitzonderingen |
| Privacy officer | Geen controle op pseudonimisering | Audit trail met classificatie per detectie |

3 regels plus een deterministische pseudonimiseringsrichtlijn-engine. Rule API op
poort 8493. De interne datasetmeting is geen onafhankelijke nauwkeurigheidsaudit;
productiegebruik vereist een vooraf geregistreerde gold set en juridische review.

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Griffier | PII classificeren handmatig | V4.2 engine classificeert automatisch |
| Privacy officer | PII lekken in publicaties | Engine herkent false positives (professionals/overheid) |
| Auditor | Geen trail van pseudonimiseringsbeslissingen | Audit trail met calculationId + hashes |
| Data scientist | Wil PII-scan integreren | Engine als Python module importeerbaar |
