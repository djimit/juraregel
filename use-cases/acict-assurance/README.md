# AcICT Assurance

Evidence-self-assessment voor de richtinggevende toetskaders van het
Adviescollege ICT-toetsing. Deze use case geeft geen AcICT-oordeel en berekent
geen compliance-score.

## Inhoud

- `profiles/projecten-2026.json`: geselecteerde projectaspecten voor JuraRegel.
- `profiles/beheer-onderhoud-2025.json`: geselecteerde beheer- en onderhoudsaspecten.
- `assessments/juraregel-projecten-2026.json`: voorlopige self-assessment.
- `assess.py`: controleert of ieder aspect voldoende bewijs, eigenaarschap en
  reviewmetadata heeft.

De evaluator retourneert per aspect `satisfied`, `not_satisfied`,
`insufficient_evidence` of `not_applicable`. Het assessment wordt pas
`review-ready` wanneer alle aspecten volledig zijn onderbouwd; anders is het
`evidence-incomplete`.

```bash
python3 use-cases/acict-assurance/assess.py \
  use-cases/acict-assurance/profiles/projecten-2026.json \
  use-cases/acict-assurance/assessments/juraregel-projecten-2026.json
```

Het meegeleverde JuraRegel-assessment is bewust `evidence-incomplete`: een
onafhankelijke review en organisatorisch bewijs voor onder meer beheer,
continuiteit en risicoacceptatie ontbreken nog.
