# NORA Use Case — Meta-laag voor Architectuur Compliance

## User Story

**Als** enterprise architect bij een overheidsorganisatie **wil ik** automatisch valideren of mijn oplossing voldoet aan NORA principes **zodat** ik NORA compliance kan bewijzen met verwijzingen naar de specifieke JuraRegel use cases die elk principe invullen.

| Rol | Probleem | Oplossing |
|---|---|---|
| Enterprise architect | NORA compliance handmatig per principe checken | Rule API checkt 15 NORA principes |
| CIO | Onduidelijk welke NORA principes nog open staan | NORA compliance matrix met gebruik cases |
| TOGAF architect | NORA principes niet gekoppeld aan implementatie | Matrix mapped principes → JuraRegel use cases |
| Bestuurder | NORA compliance niet aantoonbaar | Audit trail per principe met bronverwijzing |

## NORA als Meta-laag

NORA is niet use case #8 — NORA is de **overkoepelende architectuurlaag** die alle andere use cases verbindt:

| NORA Principe | Gekoppelde Use Cases |
|---|---|
| Gebruik open standaarden | Forum Standaardisatie, Overheidsstandaarden |
| Dienstverlening digitaal | Griffierecht, Procesreglement, Classificatie |
| Beveiliging is basisvoorwaarde | BIO2, Publicatie (PII) |
| Identiteit en toegang | Overheidsstandaarden (OAuth/OIDC) |
| Privacy by design | Publicatie (pseudonimisering) |
| API standaardisatie | Overheidsstandaarden (API Design Rules) |
| Event-driven architectuur | Overheidsstandaarden (CloudEvents) |
| Beveiligde gegevensuitwisseling | Overheidsstandaarden (Digikoppeling) |
| Sovereignty en autonomie | BIO2 |

## 15 NORA Principes

| Categorie | Aantal | Voorbeelden |
|---|---|---|
| Architectuur | 5 | Open standaarden, reuse, transparantie, API standaardisatie, continue verbetering |
| Serviceorientatie | 4 | Digitaal, gemeenschappelijke voorzieningen, events, toegankelijkheid |
| Beveiliging | 4 | Beveiliging basisvoorwaarde, privacy by design, gegevensuitwisseling, sovereignty |
| Identiteit | 1 | Identiteit en toegang |
| Data | 1 | Data bij de bron |

## API Endpoints

| Endpoint | Functie |
|---|---|
| POST /v1/nora/calculate | Check NORA principe compliance |
| GET /v1/nora/principes | Lijst alle 15 principes (filter op categorie) |
| GET /v1/nora/matrix | NORA compliance matrix met use case mapping |

## Functiehuis Rijksoverheid Rollen

| Rol | Probleem | Oplossing |
|---|---|---|
| Enterprise architect | NORA compliance handmatig per principe | Rule API checkt 15 NORA principes |
| CIO | Onduidelijk welke principes open staan | NORA compliance matrix met use case mapping |
| TOGAF architect | Principes niet gekoppeld aan implementatie | Matrix mapped principes naar JuraRegel use cases |
| Bestuurder | NORA compliance niet aantoonbaar | Audit trail per principe met bronverwijzing |

## NEDERUS Koppeling

NORA is één van de vijf frameworks in het [NEDERUS](../openspec/changes/nederus-framework-v1/sources/README.md) framework. De NORA compliance matrix is direct herbruikbaar als NEDERUS mapping-input:

| NORA Principe | NEDERUS Control | Overige Frameworks |
|---|---|---|
| Grondslag-toets | NED-01 | EU AI Act Art. 9(2), BIO2 A.5-6, NIS2 Art. 21 |
| Evenredigheid | NED-02 | EU AI Act Art. 10 |
| Proportionaliteit | NED-03 | EU AI Act Art. 14 |
| Openbaarheid | NED-04 | EU AI Act Art. 13, Art. 50 |
| Verantwoordelijkheid | NED-01, NED-03 | EU AI Act Art. 9, Art. 14, BIO2 A.5-6 |

Zie de [NEDERUS NORA crosswalk](../openspec/changes/nederus-framework-v1/sources/crosswalks/nora.md) voor de volledige mapping met grondslag-niveau detail.

