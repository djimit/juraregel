# ISO 27001 ISMS Use Case — Information Security Management System

## User Story

**Als** CISO of security officer **wil ik** een volledig ISO 27001:2022 ISMS kunnen opzetten met geautomatiseerde Statement of Applicability, asset register, en risicobehandelingsplan **zodat** ik voldoe aan de 7 verplichte documenten voor ISO 27001 certificering.

## Wetelijke Basis

| Norm | Clausule | Verplichting |
|------|----------|--------------|
| ISO/IEC 27001:2022 | 4.3 | Scope van het ISMS |
| ISO/IEC 27001:2022 | 5.2 | Beleid voor informatiebeveiliging |
| ISO/IEC 27001:2022 | 6.1.2 | Risicoanalyse |
| ISO/IEC 27001:2022 | 6.1.3 | Risicobehandelingsplan |
| ISO/IEC 27001:2022 | 6.1.3d | Statement of Applicability (SoA) |
| ISO/IEC 27001:2022 | 6.2 | Doelstellingen voor informatiebeveiliging |
| ISO/IEC 27001:2022 | 8.2 | Rapport van de beoordeling van de risico's |

## De 28 Regels — 4 Categorieën

### ISMS Clausules (8 regels)

| ID | Regel | Clausule |
|----|-------|----------|
| ISMS-4.3 | Scope van het ISMS | 4.3 |
| ISMS-5.2 | Beleid voor informatiebeveiliging | 5.2 |
| ISMS-6.1.2 | Risicoanalyse | 6.1.2 |
| ISMS-6.1.3 | Risicobehandelingsplan | 6.1.3 |
| ISMS-6.1.3d | Statement of Applicability | 6.1.3d |
| ISMS-6.2 | Doelstellingen | 6.2 |
| ISMS-8.2 | Risicobeoordeling rapport | 8.2 |

### Asset Register (2 regels)

| ID | Regel | Annex A |
|----|-------|---------|
| ASSET-001 | Inventaris van activa | A.5.9 |
| ASSET-002 | Acceptabel gebruik + eigenaar | A.5.10 |

### Risicobehandeling (4 regels)

| ID | Strategie | Risico-score |
|----|-----------|--------------|
| RISK-TREAT-001 | Accepteeren | 1-4 |
| RISK-TREAT-002 | Verminderen | 5-14 |
| RISK-TREAT-003 | Vermijden | 15-20 |
| RISK-TREAT-004 | Overdragen | 5-20 |

### Statement of Applicability (14 regels)

| ID | Control | Categorie |
|----|---------|-----------|
| SOA-A.5.1.1 | Policies for information security | Organizational |
| SOA-A.5.1.2 | Information security roles | Organizational |
| SOA-A.6.3 | Information security awareness | People |
| SOA-A.7.4 | Physical security monitoring | Physical |
| SOA-A.8.1 | User endpoint devices | Technological |
| SOA-A.8.2 | Privileged access rights | Technological |
| SOA-A.8.3 | Information access restriction | Technological |
| SOA-A.8.5 | Secure authentication | Technological |
| SOA-A.8.9 | Configuration management | Technological |
| SOA-A.8.11 | Data masking | Technological |
| SOA-A.8.12 | Data leakage prevention | Technological |
| SOA-A.8.16 | Monitoring activities | Technological |
| SOA-A.8.23 | Web filtering | Technological |
| SOA-A.8.24 | Use of cryptography | Technological |
| SOA-A.8.28 | Secure coding | Technological |

## API Endpoints

| Endpoint | Functie |
|----------|---------|
| `POST /v1/iso27001/soa/generate` | Genereer SoA uit asset register |
| `GET /v1/iso27001/soa/template` | Lege SoA-template |
| `POST /v1/iso27001/risico/behandeling` | Bepaal risicostrategie |
| `GET /v1/iso27001/isms/documenten` | 7 verplichte ISMS-documenten |

## BIO2 → ISO 27001 Mapping

| BIO2 Maatregel | ISO 27001 Annex A |
|----------------|------------------|
| A.5-6: Risicoanalyse | A.5.1.1, A.6.1.1, A.6.1.2 |
| A.8: Classificatie | A.8.1, A.8.2, A.8.3 |
| A.10: Cryptografie | A.8.24, A.8.11 |
| A.11: Beschikbaarheid | A.7.1, A.7.4, A.8.16 |
| B.3: Ontwikkeling | A.8.28, A.8.9 |
| C.6-7: Incident response | A.8.16, A.8.12 |

## Relatie tot Andere Frameworks

| Framework | Relatie |
|-----------|---------|
| BIO2 | BIO2 is implementatie van ISO 27002 voor NL overheid |
| NEN 7510 | ISO 27001 + zorgspecifieke extra's |
| NIST CSF | Crosswalk-overlay (Govern, Recover) |
| AVG/GDPR | Via DPIA use case (port 8525) |
| NEDERUS | NED-06 (Secure Development) → SOA-A.8.x |

## Bronnen

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001)
- [ISO/IEC 27002:2022](https://www.iso.org/standard/75652)
- [NEN 7510](https://www.nen.nl/zorg-welzijn/ict-in-de-zorg/informatiebeveiliging-in-de-zorg)
- [BIO2](https://www.digitaleoverheid.nl/overzicht-van-alle-onderwerpen/cybersecurity/bio-en-ensia/baseline-informatiebeveiliging-overheid/)
