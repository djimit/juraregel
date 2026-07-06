# JuraRegel Source Expansion Analysis

Datum: 2026-07-06

## Huidige staat

- Git: `main` op `e83a700` (`docs: restore architecture diagram`), working tree was schoon bij start.
- JKB bij start: 655 regels, 26 domeinen.
- JKB na uitvoering eerste bouwslice: 665 regels, 27 domeinen.
- JKB na hardening/preflights: 690 regels, 30 domeinen.
- Huidige echte source connectors: BWB/wetten.overheid.nl, EUR-Lex, PLOOI, Rechtspraak, UPL, TOOI/ROO, CVDR/SRU, Woo-index/DiWoo, STTR/RTR.
- Feitelijke JREM sourceRef-domeinen: vooral `wetten.overheid.nl`, `www.bio-overheid.nl`, `www.iso.org`, `www.overheid.nl`, `modellen.jenvgegevens.nl`, `github.com`, `www.ncsc.nl`, `www.rechtspraak.nl`, `www.forumstandaardisatie.nl`, `logius-standaarden.github.io`, `www.noraonline.nl`, `developer.overheid.nl`.

De kern-gat-analyse: JuraRegel heeft al veel domeinnamen en PoC-regels, maar gebruikt nog weinig primaire bronregisters als levende input. Vooral decentrale regelgeving, productcatalogi, Woo-publicatieketens, toegankelijkheidsregisters en interoperabiliteitsassessment ontbreken als bronconnectors of als harde verificatiebron.

## Validatiekader

Een nieuwe bron is geschikt als deze:

1. Publiek en officieel is.
2. Machineleesbaar of stabiel herbruikbaar is.
3. Regels, verplichtingen, metadata of normstatus bevat.
4. Een terugkerende frictie wegneemt voor overheid, leverancier, jurist, architect, CISO, FG of burger.
5. Past binnen L1-L3 van het JuraRegel maturity model; L4 discretionair blijft buiten scope.

## Bronnen Die Nog Niet Of Onvoldoende Worden Gebruikt

| Prioriteit | Bron | Status in repo | Waarom geschikt | Eerste toepassing |
|---|---|---|---|---|
| 1 | Lokale wet- en regelgeving / CVDR via overheid.nl en SRU | Niet als connector; lokale regels niet systematisch | 102k+ lokale regelingen, gemeente/provincie/waterschap verplicht publiceren, postcode/context mogelijk | Decentrale Regelcheck |
| 2 | UPL + Samenwerkende Catalogi | Niet gebruikt | Uniforme productnamen voor rijk, provincies, waterschappen en gemeenten; JSON/CSV/XML; quarterly updates; SDG/Wmebv kenmerken | Product- en Dienstverleningscheck |
| 3 | TOOI + ROO waardelijsten | Niet als bronlaag | Canonieke overheid-organisatie-identifiers, peildatumwaardelijsten, Woo-informatiecategorieen | Bevoegd-gezag en bron-eigenaar resolver |
| 4 | DiWoo / Woo-harvester publicatievoorwaarden | Niet gebruikt | Sitemap + Woo metadata + TOOI waardelijsten; direct aansluitbaar op Woo-index | Woo Publicatieplicht Preflight |
| 5 | DSO STTR/IMTR + RTR | Omgevingswetregels bestaan, maar STTR/RTR niet als broncontract | Toepasbare regels zijn exact het zusterconcept van RegelSpraak/JREM; XSD, verificaties, DMN voorbeelden | STTR Preflight voor Omgevingswet |
| 6 | DigiToegankelijk dashboard/register | Niet gebruikt | Overheidswebsites/apps met A-E status, wettelijke verplichting, actuele dataset | Digitale Dienst Compliance Check |
| 7 | API-register + OSS-register | Deels conceptueel, geen connector | Publieke registers, OpenAPI-first, lifecycle fields `x-deprecated` en `x-sunset` | API Lifecycle Compliance Check |
| 8 | data.overheid.nl CKAN API | Use-case bestaat, connector ontbreekt | Metadata van datasets publiek beschikbaar; CC0; CKAN API | DCAT-AP-NL live validator |
| 9 | PDOK/BAG OGC API | Basisregistratie use-case bestaat, connector ontbreekt | Dagelijks bijgewerkte BAG API; locatie/adres/context voor bevoegd gezag en omgevingsregels | Locatie-context enrichments |
| 10 | EU Interoperable Europe Act 2024/903 | Niet gebruikt | Interoperability assessment verplicht sinds 2025 voor relevante trans-Europese digitale publieke diensten | Interoperability Assessment Builder |

## Beste Use Cases Die Frictie Wegnemen

### 1. Decentrale Regelcheck

Doelgroep: gemeenten, provincies, waterschappen, leveranciers van zaak-/vergunning-/productcatalogi, burgers en ondernemers.

Input:
- postcode of bestuursorgaan;
- UPL-productnaam of vrije productnaam;
- activiteit of verzoek, bijvoorbeeld evenement, terras, alcoholvergunning, subsidie, parkeerontheffing.

Bronnen:
- lokale wet- en regelgeving / CVDR;
- UPL/Samenwerkende Catalogi;
- TOOI/ROO voor bevoegd gezag;
- SRU voor collectiezoekvragen.

Output:
- toepasselijke bestuurslaag;
- relevante lokale regeling(en);
- proceduretype: aanvraag, melding, verplichting, subsidie, bezwaar;
- beslistermijn indien hard vindbaar;
- sourceRefs naar regeling, artikel en productnaam;
- `manualReviewRequired=true` bij open normen of lokale discretionaire beleidsruimte.

Waarom eerst:
- Sluit aan op de bestaande `governance/resolver.py` met rijk/provincie/gemeente/waterschap.
- Gebruikt bronnen die nu aantoonbaar ontbreken.
- Lost echte frictie op: burgers en leveranciers hoeven niet per gemeente andere termen en verordeningen te interpreteren.

### 2. Woo Publicatieplicht Preflight

Doelgroep: Woo-coordinatoren, informatiebeheerders, gemeenten/provincies/waterschappen, KOOP-aansluiters.

Input:
- documenttype;
- bestuursorgaan;
- sitemap/URL;
- metadata: informatiecategorie, documentsoort, datum, thema, organisatie-id.

Bronnen:
- Woo-index;
- DiWoo publicatievoorwaarden;
- TOOI Woo-informatiecategorieen;
- ROO/TOOI organisatielijsten.

Output:
- actief publiceren: ja/nee/wanneer;
- ontbrekende Woo metadata;
- juiste TOOI waardelijstwaarden;
- sitemap/harvester-ready status;
- bronverwijzing naar Woo, DiWoo en TOOI.

Waarom:
- De Woo-index bestaat, maar aansluiting en metadata blijven frictie.
- JuraRegel kan precies het gat vullen tussen juridische verplichting en machineleesbare publicatievoorwaarde.

### 3. STTR Preflight Voor Omgevingswet

Doelgroep: gemeenten, waterschappen, omgevingsdiensten, softwareleveranciers.

Input:
- toepasbare-regelbestand of regelmetadata;
- activiteit/locatie;
- bevoegd gezag;
- gewenste DSO/RTR versie.

Bronnen:
- STTR/IMTR;
- RTR aansluitvoorwaarden;
- STOP/TPOD;
- lokale omgevingsplannen/omgevingsverordeningen.

Output:
- STTR-versie fit;
- veldlengte/verificatieproblemen;
- ontbrekende annotaties;
- Digikoppeling/RTR aansluitcheck;
- mapping naar JREM sourceRefs.

Waarom:
- STTR is functioneel hetzelfde probleemgebied als RegelSpraak/JREM: juridische regels begrijpelijk en uitvoerbaar maken.
- Het reduceert DSO-afkeur en leverancier-frictie zonder de hele Omgevingswet te automatiseren.

### 4. Digitale Dienst Compliance Check

Doelgroep: product owners, service managers, architecten, developers.

Input:
- URL van dienst, API of productpagina;
- organisatie;
- productnaam;
- eventueel OpenAPI URL.

Bronnen:
- UPL/Samenwerkende Catalogi;
- DigiToegankelijk dashboard/register;
- API-register;
- OSS-register;
- data.overheid.nl;
- Forum Standaardisatie.

Output:
- juiste UPL-productnaam;
- SDG/Wmebv/relevante kenmerken;
- toegankelijkheidsstatus A-E;
- API-register aanwezig en lifecycle correct;
- DCAT/API/OpenAPI conformiteit;
- concrete ontbrekende acties.

Waarom:
- Bundelt meerdere losse compliance-stappen in een preflight.
- Past direct bij bestaande JuraRegel domeinen: overheidsstandaarden, data-overheid-dcat, api-registratie, nora, forumstandaardisatie.

### 5. Interoperability Assessment Builder

Doelgroep: enterprise architecten, beleidsmakers, Europese programma's, publieke dienstverleningsketens.

Input:
- publieke digitale dienst;
- grensoverschrijdend effect;
- betrokken bestuurslagen;
- gebruikte standaarden, API's en registers.

Bronnen:
- EU 2024/903 Interoperable Europe Act;
- EIF;
- NORA;
- Forum Standaardisatie;
- API-register;
- TOOI.

Output:
- machineleesbare assessment;
- juridische, organisatorische, semantische, technische en governance-impact;
- ontbrekende interoperability solutions;
- publiceerbare rapportage.

Waarom:
- Dit is een architectuur-use-case met hoog strategisch gewicht en weinig privacyrisico.
- Past bij Dennis' TOGAF/NORA/Forum-profiel en bij JuraRegel als cross-government control plane.

## Aanbevolen Eerste Bouwslice

Niet meteen vijf use cases bouwen. De kleinste zinvolle slice:

1. Maak een bronconnector voor UPL.
2. Maak een bronconnector voor TOOI/ROO waardelijsten.
3. Maak een minimale `dienstverlening-check` use case:
   - input: `organisatie`, `productNaam`, `bestuurslaag`;
   - output: uniforme productnaam, bestuurslaagfit, SDG/Wmebv flags, sourceRefs;
   - 8-12 regels, 6 tests, L1.
4. Daarna pas CVDR/SRU erbij voor lokale regelteksten.

Reden: UPL/TOOI is gestructureerd, stabiel, officieel en direct toepasbaar. CVDR is waardevoller maar rommeliger; eerst de product- en organisatie-as hard maken.

## Niet Nu Doen

- Geen generieke AI-extractor voor alle lokale regelingen.
- Geen volledige Omgevingswet/DSO clone.
- Geen nieuwe vectorstack.
- Geen nieuwe governance layer.

Eerst bronhardheid en een werkende preflight. Daarna opschalen.
