# Judicial AI Admission And Evidence Gate

## Doel en claimgrens

Deze demo laat zien hoe Djimit bewijs rond een complexe AI-use-case kan
structureren. Zij bewijst niet dat een systeem juridisch compliant, veilig of
geschikt voor productie is.

De demo houdt vier bewijslagen uit elkaar:

| Laag | Systeem | Bewijst | Bewijst niet |
|---|---|---|---|
| Normatief contract | JuraRegel | Welke evidence het profiel verlangt | Definitieve juridische juistheid |
| Modelgedrag | OpenMythos | Gedrag onder vastgelegde tests | Rechtskwaliteit of compliance |
| Uitvoering | Djimitflo | Runs, capabilities, acties en approvals | Kwaliteit van menselijke beoordeling |
| Eindbeslissing | Bevoegde mens | Wie binnen scope toestemming gaf | Garantie tegen schade of fouten |

## Uitkomsten

- `blocked`: ten minste één hard stop mist evidence, heeft gefaalde evidence of
  de menselijke eindbeslissing is afwijzend.
- `review-required`: automation heeft evidence gevonden, maar kan deze niet
  juridisch accepteren of de menselijke eindbeslissing ontbreekt.
- `conditionally-admissible`: alle vereiste evidence is aanwezig en een
  expliciete goedkeuring verwijst naar exact dezelfde profielversie.

Er bestaat geen gemiddelde score. Een goede modelbenchmark kan een ontbrekende
waarborgen voor rechterlijke bevoegdheid, bronlineage of formele autorisatie
nooit compenseren.

## NEDERUS Koppeling

Het Judicial AI Assurance profiel raakt meerdere frameworks. De NEDERUS controls
(NED-01 t/m NED-05) bieden de multi-jurisdictionele mapping:

| NEDERUS Control | Relevantie voor Judicial AI |
|---|---|
| NED-01 AI Impact Assessment | Vereist vóór inzet AI in rechterlijke context |
| NED-03 Human Oversight | Essentieel: rechterlijke autonomie vereist menselijke regie |
| NED-04 Transparency | Bronherleidbaarheid voor rechterlijke besluitvorming |

Zie [NEDERUS use case](../docs/nederus-use-case.md) voor de volledige mapping.

## Genereren

```bash
.venv/bin/python use-cases/judicial-ai-assurance/demo/admission_gate.py
```

Invoer:

- `jrem/exports/judicial-ai-assurance-2026.1.json`: de canonieke controls;
- `demo/scenarios.json`: synthetische evidence en negatieve controles.

Uitvoer:

- `playground/judicial-ai-demo.json`: portable, deterministische evidence pack;
- `playground/judicial-ai.html`: dependency-free viewer.

De tests regenereren de pack in memory en eisen exacte gelijkheid met het
gecommitte bestand. Een profiel- of scenariowijziging kan daardoor niet stil
een verouderde demo publiceren.

## Evidence-adaptercontract

Een adapter schrijft geen nieuwe juridische conclusie. Hij normaliseert een
bestaand bewijsstuk naar:

```json
{
  "sourceSystem": "openmythos",
  "status": "observed",
  "runId": "immutable-run-id",
  "artifactRef": "system://path/or/run/id",
  "summary": "Feitelijke beschrijving zonder juridische goedkeuring",
  "artifactTypes": ["independent-evaluation", "task-specific-gold-set"]
}
```

De generator voegt een canonieke SHA-256-hash van het genormaliseerde record
toe. Een productie-adapter levert daarnaast de hash van het ruwe artifact of
een immutable run-ID. `observed` betekent alleen
dat evidence bestaat. `failed` betekent dat de bronrun zelf een negatieve
bevinding rapporteerde. Alleen de menselijke eindgate kan evidence accepteren.

De meegeleverde bestand-adapters kunnen zonder netwerktoegang worden uitgevoerd:

```bash
.venv/bin/python use-cases/judicial-ai-assurance/demo/evidence_adapter.py \
  openmythos RUN.jsonl --oracle ORACLE.jsonl --run-id IMMUTABLE_RUN_ID

.venv/bin/python use-cases/judicial-ai-assurance/demo/evidence_adapter.py \
  djimitflo EXPORTED_RUN.json
```

Zij lezen alleen exports, berekenen een hashmanifest van de ruwe bestanden en
schrijven één genormaliseerd pre-record naar stdout. De generator voegt daarna
het sequentiële `id` en de canonieke `recordHash` toe; dan voldoet het record
exact aan het evidence-schema. De OpenMythos-oracle-export wordt
inhoudelijk gecontroleerd en zit samen met de run-export in de berekende
bundelhash. Voor productie moeten beide bronbestanden immutable worden opgeslagen.

### OpenMythos

Minimaal vereist:

- run-, model- en providerversie;
- corpus-, prompt- en configuratiehash;
- case-resultaten en gebruikte scoring source;
- transport- en completionstatus;
- verwijzing naar het ongewijzigde ruwe artifact.

De adapter verwerkt JSONL-run- en oracle-exports. Een expliciet negatieve,
toepasselijke oracle-uitkomst wordt `failed`; een algemene modelscore wordt
nooit omgezet naar een JuraRegel-goedkeuring.

### Djimitflo

Minimaal vereist:

- evaluation-, loop- en trace-ID's;
- capability grants en denials;
- model-, prompt- en toolversies;
- checkpoint/replayrelaties indien gebruikt;
- afzonderlijke validatie- en autorisatie-events.

De adapter verwerkt een JSON-export van exact één evaluation-run. Ook een lage
of hoge `overall_score` blijft slechts `observed` zolang de bronrun voltooid is:
de adapter bevat bewust geen scoregrens. Een logregel `approved=true` is
onvoldoende zonder actor, rol, scope,
profielversie en een afzonderlijke bevoegde autorisatie.

### Wiki en Knowledge

Wiki- en knowledgebronnen zijn discovery-input. Een gevonden bron wordt pas
normatief bruikbaar nadat zij in het JuraRegel source register is geclassificeerd
en de normale juridische review heeft doorlopen.

## Publiceren en integreren

### GitHub Pages

De bestaande workflow publiceert de volledige `playground/` map wanneer `main`
wijzigt. Er is geen extra build, secret of runtime nodig.

Verwachte route na een goedgekeurde merge:

```text
https://djimit.github.io/juraregel/judicial-ai.html
```

### Djimit.nl

De kleinste integratie is een link naar de GitHub Pages-demo. Wanneer dezelfde
huisstijl of analytics nodig zijn, kan Djimit.nl daarna één van deze bestaande
artifacts hergebruiken:

```text
playground/judicial-ai.html
playground/judicial-ai-demo.json
```

Mogelijke integraties, in voorkeursvolgorde:

1. link naar de standalone demo;
2. iframe binnen een Djimit.nl-casepagina;
3. client-side fetch van de JSON en rendering met het bestaande design system.

Er is geen afzonderlijke API nodig zolang de demo alleen gecommitte,
synthetische evidence toont.

## Verificatie

```bash
.venv/bin/python -m pytest \
  use-cases/judicial-ai-assurance/tests/test_judicial_ai_assurance.py -q

bash ci/run-gates.sh use-cases/judicial-ai-assurance
bash ci/run-all-gates.sh
```

Voor een lokale HTTP-smoke:

```bash
python3 -m http.server 8765 --directory playground
curl -f http://127.0.0.1:8765/judicial-ai.html
curl -f http://127.0.0.1:8765/judicial-ai-demo.json
```

## Human final gate

De demo bevat bewust geen UI-knop die een echte toelating simuleert. Juridische,
governance-, security-, publicatie-, commerciële en Git-beslissingen staan in
`goals/judicial-ai-admission-evidence-demo/HUMAN_GATES.md`.
