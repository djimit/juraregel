# JuraRegel enterprise-grade level-3 plan

**Baseline:** 2026-07-30
**Normatieve status:** uitvoerings- en bewijsplan; geen certificering
**Bronaudit:** [repository-ecosystem audit](audit/REPOSITORY-ECOSYSTEM-AUDIT-2026-07-30.md)
**Beslisregel:** een control is alleen voldaan door herhaalbaar bewijs met een
afgebakend subject, versie, observatiemethode, falsificatieconditie en
geldigheidsduur.

## 1. Doel en wetenschappelijke maatstaf

Het doel is niet “veel enterprise-features”, maar een systeem waarvan elke
materiële claim controleerbaar waar, begrensd en reproduceerbaar is. Level 3
betekent hier:

1. **L3 legal maturity:** regels zijn machineleesbaar, scenario-getest,
   brontechnisch traceerbaar en onafhankelijk juridisch geaccepteerd.
2. **Operational assurance:** identity, data-isolatie, continuïteit en
   observability zijn op de doelomgeving beproefd.
3. **Epistemic assurance:** mapping, configuratie, unit test, integratietest,
   juridisch oordeel en productie-observatie worden niet met elkaar verward.
4. **Reproducibility:** bewijs bevat code-, bron-, corpus-, configuratie- en
   artifact-identiteit en kan door een onafhankelijke partij worden herhaald.

Een gewogen compliancescore is bewust uitgesloten. Een gemiddelde kan een
ontbrekende hard-stop maskeren. JuraRegel gebruikt daarom per control slechts
`satisfied`, `not_satisfied` of `blocked_external`, met conjunctieve promotie:

```text
review-ready =
  alle repository-controls satisfied
  EN alle toepasselijke externe controls satisfied
```

## 2. Auditbevinding naar closure

| ID | Auditbevinding | Risico | Repository-closure | Bewijs/exit |
|---|---|---|---|---|
| A-01 | `insufficient_evidence` kon review-ready worden | vals assurance-oordeel | intrinsieke evidence-, risico-, eigenaar- en reviewvalidatie | negatieve assessortests |
| A-02 | lokale categorieën golden als OpenMythos-observatie | tautologische dekking | observed corpus en lokale mapping gescheiden | versie + corpus-hash in evidence snapshot |
| A-03 | Djimitflo-bridge was alleen in-memory | fictieve integratieclaim | status blijft `evidence-incomplete` | pas sluiten met persistente idempotente run |
| A-04 | canonical gate sloeg root/API-tests over | regressies buiten CI | alle testoppervlakken in lokale en GitHub-gate | gate-uitvoer |
| A-05 | acht Markdown-links waren kapot | documentatiecontract onbetrouwbaar | repositorybrede linkchecker | nul ontbrekende targets |
| A-06 | 23 checks retourneerden hardcoded succes | zelfreferentiële Grade A | alle checks fail-closed zonder reviewbaar runtimebewijs | truth-boundary tests |
| A-07 | ISO 27017-profiel miste planvelden | niet-reproduceerbare beoordeling | subject, scope, artifacts, rollen en mappings gestructureerd | schema- en assessortests |
| A-08 | publicaties bevatten onbewezen totalen | schijnprecisie | waarschuwingen en versieerbaar empirisch bewijs vereist | Markdown- en claimreview |
| A-09 | recente JLAIF-workflow was rood | niet-herhaalbare assurance | Ruff-debt op exact workflowoppervlak opgelost | dezelfde lint- en benchmarkcommands |
| E-01 | permissieve bearer/API-key/JWT-paden | authenticatie-bypass | alleen cryptografisch geverifieerde JWT/OIDC of expliciete service-key | security-contracttest |
| E-02 | readiness rapporteerde afwezige diensten als gezond | foutieve deploypromotie | actieve PostgreSQL- en Qdrant-probes | `/ready` negatief en positief testen |
| E-03 | Compose bevatte lokale infrastructuur/credentials | secret- en portabiliteitsrisico | verplichte externe configuratie en loopback-publicatie | `docker compose config` |
| E-04 | container draaide als root en installeerde ambigu | supply-chain/runtime privilege | minimale requirements, vaste versies, non-root UID | image inspect + build |
| E-05 | app maakte productietabellen automatisch | ongecontroleerde schemamutatie | `create_all` uitsluitend development | lifespan-contracttest |
| E-06 | in-memory limiter met twee workers | omzeilbare limiet | productie vereist goedgekeurde ingress | configuratie-negatieftest |
| E-07 | documentatie claimde generieke RLS | onjuist isolatiebewijs | claim begrensd; per endpoint/deployment bewijs vereist | doc- en autorisatiereview |

## 3. Target assurance architecture

De architectuur kent vijf bewijsniveaus. Een hoger niveau mag nooit uit een
lager niveau worden afgeleid:

| Niveau | Vraag | Minimumbewijs |
|---|---|---|
| Syntactisch | is het artifact valide? | schema, compile, link- en lintgate |
| Semantisch | doet de regel wat is gespecificeerd? | positieve, negatieve en grensscenario's |
| Juridisch | is interpretatie en toepasselijkheid aanvaard? | onafhankelijke reviewer, versie, datum, scope |
| Operationeel | werkt de keten op de doelomgeving? | getekende run lineage, request/response-hashes, telemetry |
| Institutioneel | is beheer duurzaam en accountable? | eigenaar, SLO, incident-, wijzigings- en exitproces |

De trust boundaries zijn:

- bronhouder naar JREM-extractie;
- rule/evidence artifact naar evaluator;
- gebruiker/service naar API en tenantcontext;
- API naar PostgreSQL, Qdrant, Keycloak en LLM;
- JuraRegel naar OpenMythos en Djimitflo;
- build naar image registry en deployment.

Voor iedere boundary gelden authenticiteit, integriteit, herleidbaarheid,
minimale bevoegdheid, replay-bestendigheid en expliciete failure semantics.

## 4. Uitvoeringsprogramma

### Fase 0 — waarheid en reproduceerbaarheid

**Doel:** voorkom dat documentatie of tests meer suggereren dan zij aantonen.

- Leg claims vast als `{subject, version, scope, method, evidence,
  falsification, validUntil}`.
- Laat ontbrekende hard-stop-evidence altijd falen.
- Scheid static mapping coverage van runtime-integratie.
- Blokkeer kapotte Markdown en niet-uitgevoerde testoppervlakken in CI.
- Markeer historische cijfers als niet-reproduceerbaar totdat case-level data
  en analysescripts beschikbaar zijn.

**Exit:** A-01 t/m A-09 zijn door de canonical gate reproduceerbaar gesloten.

### Fase 1 — veilige productiegrens

**Doel:** de repository kan niet stilzwijgend onveilig als productie starten.

- Vereis PostgreSQL, Qdrant, Keycloak, expliciete CORS en ingress-rate-limit.
- Verwerp unsigned JWT en ingebedde service credentials.
- Voer geen productiemigraties of schema-aanmaak uit tijdens app-start.
- Draai images non-root; bind lokale Compose-poorten uitsluitend aan loopback.
- Laat readiness echte afhankelijkheden bevragen.
- Behandel tenantcontext niet als autorisatiebewijs. Iedere persistente route
  krijgt een expliciete object-, rol- en tenantautorisatietest voordat zij voor
  productie wordt geactiveerd.

**Exit:** E-01 t/m E-07 zijn gesloten; containerbuild en configuratie slagen;
negatieve auth/readiness/configuratieprobes falen zoals ontworpen.

### Fase 2 — data-integriteit en tenantisolatie

**Doel:** maak PostgreSQL de gezaghebbende store voor geactiveerde
productieroutes.

- Inventariseer route voor route welke store werkelijk wordt gebruikt.
- Activeer alleen routes met transacties, migraties, constraints, tenantfilter
  en RLS-policy.
- Test twee tenants met identieke object-ID-patronen en bewijs dat lezen,
  wijzigen, exporteren en zoeken cross-tenant onmogelijk is.
- Maak auditrecords append-only, tijdgesynchroniseerd en voorzien van actor,
  tenant, correlation ID, input/output-hash en policyversie.
- Test migratie forward, rollbackstrategie, backup en point-in-time restore.

**Exit:** geen productieroute gebruikt procesgeheugen als system of record;
cross-tenant adversarial tests en restore-oefening slagen.

### Fase 3 — supply chain en platform operations

**Doel:** maak iedere release identificeerbaar, herstelbaar en observeerbaar.

- Pin dependency-resolutie met hashes of een goedgekeurd lockmechanisme.
- Genereer SBOM, vulnerability scan, provenance en ondertekende image digest.
- Definieer SLI/SLO voor beschikbaarheid, foutpercentage, latency,
  evidence-lag en herstelduur.
- Alarmeer op auth-falen, tenant-isolatiefalen, readiness, queue/backlog,
  evaluatiedrift en audit-write-falen.
- Voer incident-, credential-rotation-, failover- en disaster-recoverytests uit.
- Documenteer retentie, legal hold, verwijdering en exit/export.

**Exit:** ER-OPS-01 bevat deployment-specifieke, gedateerde artifacts en een
goedgekeurde eigenaar.

### Fase 4 — juridische en normatieve promotie

**Doel:** promoveer use cases op basis van onafhankelijke inhoudelijke
acceptatie.

- Registreer gezaghebbende bron, versie, geldigheid, licentie en extractiehash.
- Laat een andere bevoegde jurist dan de auteur regels en scenario's beoordelen.
- Voeg tegenvoorbeelden, uitzonderingen, temporele grenzen en
  bevoegdheidsconflicten toe.
- Voor ISO 27017: gebruik gelicentieerde ISO/NEN-tekst en onafhankelijke
  interpretatiereview; gebruik openbare samenvattingen niet als normtekst.
- Leg afwijkingen en review-expiry vast; verlopen review blokkeert promotie.

**Exit:** ER-LEGAL-01 en ER-ISO-01 zijn voldaan voor de geactiveerde scope.

### Fase 5 — OpenMythos/Djimitflo ketenbewijs

**Doel:** vervang de in-memory integratieclaim door geobserveerde lineage.

- Keur target, credential boundary en mutatiebevoegdheid vooraf goed.
- Verstuur één geauthenticeerd, idempotent event met deterministische key.
- Persisteer run, case results, broncommit, corpus-hash, timestamps en
  request/response-hashes.
- Test success, replay, timeout, gedeeltelijke write en herstel.
- Verifieer dat een onafhankelijke query dezelfde lineage terugleest.

**Exit:** ER-ECO-01 wordt uitsluitend `satisfied` wanneer het gedateerde
evidence artifact `conclusion=verified` bevat en de onderliggende records
herhaalbaar uitleesbaar zijn.

## 5. CI/CD promotion policy

| Stage | Blokkerende gates |
|---|---|
| Pull request | schema, compile, lint, links, unit/negative tests, source quality |
| Merge | volledige canonical gate, JLAIF regressie/challenge/drift/canary |
| Release candidate | containerbuild, SBOM/scan/provenance, migratie- en contracttests |
| Staging | OIDC, tenantisolatie, dependency probes, restore en failure injection |
| Production | `enterprise_readiness.py --enforce` plus menselijke change approval |

Bewijs wordt bij voorkeur als immutable CI-artifact vastgelegd. Een groene
oude run geldt niet voor een nieuwe commit, bronversie, corpusversie of
deploymentconfiguratie.

## 6. Governance en verantwoordelijkheden

| Rol | Niet-delegeerbare verantwoordelijkheid |
|---|---|
| Product owner | toepasselijke scope en risicotolerantie |
| Juridisch eigenaar | interpretatie, uitzonderingen en geldigheid |
| Security owner | threat model, identity, secrets en incidentacceptatie |
| Data owner | classificatie, retentie, tenantgrens en export |
| Platform owner | SLO, backup, restore, patching en deployment |
| Onafhankelijke reviewer | falsificatie en acceptatie buiten auteursrol |

Geen enkele technische test mag de juridische reviewer vervangen; geen
juridische review mag operationeel ketenbewijs vervangen.

## 7. Evidence contract en stopcriteria

Elk extern bewijsartifact bevat minimaal:

```json
{
  "controlId": "ER-...",
  "subject": "immutable identifier",
  "version": "source or deployment version",
  "scope": ["bounded component"],
  "observedAt": "RFC3339 timestamp",
  "method": "reproducible procedure",
  "evidence": ["immutable artifact reference"],
  "result": "satisfied | not_satisfied",
  "reviewer": "accountable independent party",
  "validUntil": "RFC3339 timestamp or explicit event boundary"
}
```

Stop en degradeer de status wanneer:

- bewijs ontbreekt, verloopt of niet meer bij subject/versie past;
- een afhankelijkheid alleen via mock of configuratie is bewezen;
- audit logging of tenantisolatie faalt;
- bron-, corpus- of modelversie wijzigt zonder herbeoordeling;
- een externe mutatie niet vooraf is goedgekeurd.

## 8. Huidige closure en resterende poorten

`python3 ci/enterprise_readiness.py` rapporteert repositoryproblemen en externe
poorten afzonderlijk. De reeds gecorrigeerde auditproblemen maken de huidige
prototypes aantoonbaar betrouwbaarder. Proceslokale routes zijn uitgesloten van
productie, supply-chain bewijs is aan CI toegevoegd en brondebt kan niet naar
L2/L3 promoveren. Volledige promotie blijft geblokkeerd op:

- ER-ECO-01: geautoriseerde persistente OpenMythos/Djimitflo-run;
- ER-LEGAL-01: onafhankelijke L2/L3-juridische acceptatie;
- ER-ISO-01: gelicentieerde ISO/NEN-bron en onafhankelijke review;
- ER-OPS-01: doelomgeving-specifieke security-, SLO-, backup- en DR-bewijzen.

Deze poorten zijn geen toekomstige features die met extra code kunnen worden
“opgelost”. Zij vereisen externe autoriteit en empirisch bewijs.
