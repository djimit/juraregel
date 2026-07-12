# JuraRegel Presentatie Outline (15 min, 5 slides)

> **Archief — niet gebruiken als actuele productclaim.** Zie de capability- en
> maturity-status in de repository-README; cijfers hieronder zijn historisch en
> niet onafhankelijk gevalideerd.

## Slide 1: Het Probleem (3 min)
- Nederlandse overheidsregels staan in PDFs, niet in code
- Compliance checking is handmatig, foutgevoelig, niet-auditeerbaar
- 174.210 uitspraken, 25.127 met PII, 14,4%

## Slide 2: De Oplossing (3 min)
- JuraRegel: regels die juristen schrijven en computers begrijpen
- RegelSpraak CNL → JREM → CI/CD → Rule API
- 16 use cases, 444 regels, 10 domeinen

## Slide 3: Wat Bewezen Is (4 min)
- Pseudonimiseringsrichtlijn engine V4.2: 100% op 25K uitspraken
- Engine evolutie: V1 (95%) → V4.2 (100%)
- 59% false positives herkend (professionals/overheid)
- Reproduceerbaar

## Slide 4: Wat Je Krijgt (3 min)
- SDK, CLI, Docker, Helm, GitHub Actions, playground, dashboard
- Templates: ADR, threat model, DPIA, user story
- 16 functiehuis rollen gedekt

## Slide 5: Hoe Verder (2 min)
- Repo: github.com/djimit/juraregel
- Playground: djimit.github.io/juraregel
- CONTRIBUTING.md voor nieuwe use cases
- MIT license
