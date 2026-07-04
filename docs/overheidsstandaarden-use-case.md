# Overheidsstandaarden Use Case — API, Authenticatie, Events en Digikoppeling

## User Story

**Als** API architect bij een overheidsorganisatie **wil ik** automatisch valideren of mijn APIs en services voldoen aan de Logius en Forum Standaardisatie standaarden **zodat** ik niet handmatig 24 regels hoef te checken en developer.overheid.nl registratie foutloos is.

| Rol | Probleem | Oplossing |
|---|---|---|
| API architect | API Design Rules handmatig checken per endpoint | Rule API checkt per regel: compliant ja/nee |
| Security engineer | OAuth/OIDC profiel niet volledig geïmplementeerd | Check NL GOV Assurance Profile OAuth 2.0 regels |
| Event architect | CloudEvents formaat niet conforme | Check NL GOV Profile for CloudEvents regels |
| Integratie architect | Digikoppeling cert/protocol onduidelijk | Check WUS/ebMS/certificaat regels |
| developer.overheid.nl | API niet geregistreerd | Check OpenAPI 3.0 + registratie regels |

## Standaarden per categorie

| Categorie | Aantal | Bron | Voorbeelden |
|---|---|---|---|
| API Design | 14 | Logius | RESTful, HAL, JSON, error responses, versioning, pagination, CORS, HTTPS |
| Authenticatie | 4 | Forum Standaardisatie + Logius | OAuth 2.0 NL GOV, eIDAS SAML, OIDC, JWT |
| Events | 3 | Logius | CloudEvents structured mode, extensies |
| Digikoppeling | 3 | Logius | WUS 3.0, ebMS 3.0, PKIoverheid certificaten |
| developer.overheid.nl | 2 | developer.overheid | API registratie, OpenAPI 3.0 |
| **Totaal** | **24** | | |

## API Endpoints

| Endpoint | Functie |
|---|---|
| POST /v1/overheidsstandaarden/calculate | Check standaard compliance |
| GET /v1/os/standaarden | Lijst alle standaarden (filter op categorie/bron) |
| GET /v1/os/rapport/{orgId} | Compliance rapport per organisatie |

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| API architect | API Design Rules handmatig per endpoint | Rule API checkt 14 API regels |
| Security engineer | OAuth/OIDC profiel incompleet | Check NL GOV Assurance Profile OAuth 2.0 |
| Event architect | CloudEvents niet conforme | Check NL GOV Profile for CloudEvents |
| Integratie architect | Digikoppeling protocol onduidelijk | Check WUS/ebMS/certificaat regels |

