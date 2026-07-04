# Forum Standaardisatie Use Case — Verplichte Open Standaarden

## Overzicht

De Forum Standaardisatie use case voegt de verplichte open standaarden toe als zesde use case. Met 22 standaarden (16 verplicht + 6 streefbeeld) bewijst deze use case dat JuraRegel niet alleen beveiligingsregels (BIO2) of rechtspraakregels (griffierecht) kan automatiseren, maar ook interoperabiliteitsstandaarden.

## User Story

**Als** architect van een overheidsorganisatie **wil ik** automatisch valideren of mijn organisatie de verplichte open standaarden toepast **zodat** ik niet handmatig de Forum Standaardisatie lijst hoef te checken en Monitor-rapportage foutloos is.

| Rol | Probleem | Oplossing |
|---|---|---|
| Architect | 22 standaarden handmatig bijhouden — verouderd | Rule API checkt per standaard: compliant ja/nee |
| CIO | Onduidelijk welke verplichte standaarden ontbreken | Compliance rapport per categorie |
| Forum Standaardisatie | Geen gestandaardiseerd controle-instrument | JuraRegel als open-source compliance tool |
| Monitor-verantwoordelijke | Handmatige rapportage inconsistent | `GET /v1/fs/rapport/{orgId}` — Monitor aligned |

## Standaarden

| Categorie | Verplicht | Streefbeeld |
|---|---|---|
| Interoperabiliteit | 5 (OAuth, SAML, OData, StUF, ebMS) | 3 (Common Ground, NORA, HBA) |
| Veiligheid | 5 (DKIM, DMARC, SPF, TLS, DNSSEC) | 3 (ISO 27001, BIO2, NCSC) |
| Document | 4 (PDF, OOXML, ODF, eFactuur) | — |
| Identiteit | 2 (eIDAS, iGOV) | — |
| **Totaal** | **16** | **6** |

## API Endpoints

| Endpoint | Functie |
|---|---|
| POST /v1/forumstandaardisatie/calculate | Check standaard compliance |
| GET /v1/fs/standaarden | Lijst alle standaarden met filter |
| GET /v1/fs/rapport/{orgId} | Monitor Open Standaarden aligned rapport |
| GET /v1/health | Healthcheck |

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Architect | 22 standaarden handmatig bijhouden | Rule API checkt per standaard: compliant ja/nee |
| CIO | Onduidelijk welke verplichte standaarden ontbreken | Compliance rapport per categorie |
| Forum Standaardisatie | Geen gestandaardiseerd controle-instrument | JuraRegel als open-source compliance tool |
| Monitor-verantwoordelijke | Handmatige rapportage inconsistent | GET /v1/fs/rapport/{orgId} — Monitor aligned |

