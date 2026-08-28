# Informatiehuishouding Assurance

Niet-scorend evidenceprofiel voor de sturing en beheersing van de
informatiehuishouding binnen de Rijksoverheid. Het profiel combineert het
Meerjarenplan 2026-2030 met recente ADR-bevindingen en gebruikt het
Meerjarenplan 2024-2025 uitsluitend als historische baseline.

De bronnen zijn beleid, onderzoeksbevindingen en handelingsperspectieven. Ze
zijn geen rechtsregels, certificering of bewijs dat een organisatie haar
informatiehuishouding beheerst.

## Inhoud

- `sources/source-register.json`: vijf officiële documenten met versie, rol,
  retrievaldatum en SHA-256.
- `profiles/rijk-ihh-2026.json`: tien lokale evidence-aspecten met exacte
  bronankers, vereiste bewijsstukken en falsificatiecriteria.
- `tests/test_informatiehuishouding_assurance.py`: bewaakt bronlineage en de
  fail-closed, non-scoring grens.

Het bestaande ADR ITGC-kader blijft een afzonderlijke catalog-only use case.
Een ITGC-maatregel of volwassenheidsscore bewijst niet dat een aspect uit dit
profiel is voldaan. Bij toepassing kan het bestaande evidence-assessment uit
`use-cases/acict-assurance/assess.py` worden hergebruikt; zonder volledig
organisatiebewijs en onafhankelijke review blijft de uitkomst
`evidence-incomplete`.
