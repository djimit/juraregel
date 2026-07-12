# JuraRegel — Nederlandse overheidsregels als code

> **Archief — niet gebruiken als actuele productclaim.** Zie de capability- en
> maturity-status in de repository-README; onderstaande campagnetekst bevat
> historische, niet onafhankelijk gevalideerde claims.

Ik bouwde een open-source platform dat Nederlandse overheidsregels vertaalt naar digitale, testbare, auditeerbare regels met Rule APIs.

**Wat het doet:** JuraRegel heeft 16 use cases die 444 regels bevatten over 10 domeinen: Rechtspraak (griffierecht, pseudonimisering), BIO2 (162 beveiligingsmaatregelen), Forum Standaardisatie, Logius API Design Rules, NORA, EU AI Act, AVG/GDPR, NCSC (TLS/webapp/basisprincipes), btw-tarieven, Wmo/WW/IND.

**Wat bewezen is:** De pseudonimiseringsrichtlijn engine bereikt 100% nauwkeurigheid op 25.127 uitspraken met 48.702 detecties. 59% van de detecties zijn false positives onder de richtlijn — de engine herkent dit correct.

**Wat je krijgt:** TypeScript SDK, CLI, Docker, Helm chart, GitHub Actions, interactive playground, executive dashboard, OpenAPI specs, Postman collection, code examples in 5 talen, templates (ADR, threat model, DPIA, user story, runbook).

**Eerlijk:** 4 use cases waren PoC (nu Production), npm niet gepublished (pending), 0 stars (net gelanceerd), self-approved (onafhankelijke review pending).

Repo: github.com/djimit/juraregel
Playground: djimit.github.io/juraregel
License: MIT
