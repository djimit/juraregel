# Legal AI Assurance Framework (JLAIF)

> Een verifieerbare juridische beslis- en bewijsinfrastructuur waarin AI alleen opereert binnen aantoonbare grenzen.

## 1. Federatief Governance Model

### 1.1 Architectuur

Het JLAIF federatieve governance-model bestaat uit drie lagen:

```
┌─────────────────────────────────────────────────────────┐
│  CENTRAAL: Legal AI Assurance Office                    │
│  - Taxonomie & standaarden                               │
│  - Minimale evaluatie-eisen                              │
│  - Severity-model (S1-S5)                                │
│  - Auditvereisten                                        │
│  - Leveranciersvoorwaarden                               │
│  - Incidentregistratie                                   │
│  - Referentiearchitectuur                                │
│  - Release gates                                         │
├─────────────────────────────────────────────────────────┤
│  DECENTRAAL: Juridische Domeinteams                      │
│  - Use-case validatie                                    │
│  - Gouden datasets                                       │
│  - Uitzonderingsbeoordeling                              │
│  - Bronbeheer                                            │
│  - Acceptatietests                                       │
│  - Productiecontrole                                     │
├─────────────────────────────────────────────────────────┤
│  ONAFHANKELIJK: Tweede & Derde Lijn                      │
│  - Risk, Privacy, Security, Compliance                   │
│  - Internal Audit / Externe evaluator                    │
│  - Ethische / Maatschappelijke Raad                      │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Centraal: Legal AI Assurance Office

Het centrale bureau stelt vast:

| Domein | Beschrijving | Frequentie |
|--------|--------------|------------|
| Taxonomie | Fouttype-classificatie (9 types) en severity levels (S1-S5) | Jaarlijks |
| Evaluatie-standaarden | Minimale benchmark-eisen per rechtsgebied | Halfjaarlijks |
| Severity-model | Impact-gewichten en release-thr | Jaarlijks |
| Auditvereisten | Wat moet auditeerbaar zijn | Jaarlijks |
| Leveranciersvoorwaarden | Benchmarkrecht, versietransparantie, incidentmelding | Continu |
| Incidentregistratie | Centrale melding van materiële fouten | Continu |
| Referentiearchitectuur | Evidence lineage, gate patterns | Halfjaarlijks |
| Release gates | Go/no-go criteria per autonomie-niveau | Per release |

### 1.3 Decentraal: Juridische Domeinteams

Elk juridisch domein (strafrecht, civielrecht, bestuursrecht, etc.) voert uit:

- **Use-case validatie**: Classificatie volgens L1-L5 autonomie-schaal
- **Gouden datasets**: Domein-specifieke testcases met geautoriseerde antwoorden
- **Uitzonderingsbeoordeling**: Edge cases die generieke benchmarks missen
- **Bronbeheer**: Actuele wetgeving, jurisprudentie, beleidsdocumenten
- **Acceptatietests**: Productie-acceptatie op domein-specifieke criteria
- **Productiecontrole**: Continue monitoring van AI-prestaties in productie

### 1.4 Onafhankelijk: Tweede en Derde Lijn

**Tweede lijn** (Risk, Privacy, Security, Compliance):
- Beoordeelt het assurance control framework
- Valideert risico-analyses en mitigerende maatregelen
- Toetst conformiteit met EU AI Act, AVG, BIO

**Derde lijn** (Internal Audit / Externe evaluator):
- Beoordeelt opzet, bestaan en werking van controls
- Onafhankelijke verificatie van benchmark-resultaten
- Rapportage aan bestuur en toezichthouder

**Ethische raad**:
- Toetst disproportionele impact op kwetsbare groepen
- Adviseert over maatschappelijke acceptatie
- Signaleert systeemrisico's

## 2. Use-case Kwalificatie (L1-L5)

| Klasse | Voorbeeld | Regime | Approvers | Djimitflo Control |
|--------|-----------|--------|-----------|-------------------|
| L1 Ondersteunend | Spelling, structurering | Lichte controles | 1 | NED-04 |
| L2 Informatief | Samenvatten, zoeken | Bronverificatie + steekproeven | 1 | NED-04 |
| L3 Adviserend | Juridische analyse, conceptadvies | Formele validatie + verplichte review | 2 | NED-01, NED-03 |
| L4 Besluitnabij | Prioritering, risicosignalering | Onafhankelijke assurance + logging | 2 | NED-01, NED-02, NED-03 |
| L5 Beslissend | Automatische juridische beslissing | Uitsluiten of zeer strikt wettelijk | 2 + extern | NED-01, NED-05 |

## 3. Multi-dimensionale Benchmark

### 3.1 Metrieken

| Metriek | Beschrijving | Minimum |
|---------|--------------|---------|
| Juridische juistheid | Correcte juridische conclusies | 90% |
| Volledigheid | Alle relevante aspecten behandeld | 85% |
| Bronjuistheid | Correcte bronverwijzingen | 95% |
| Citation entailment | Bronnen ondersteunen bewering | 90% |
| Actualiteit | Actuele wetgeving/jurisprudentie | 95% |
| Jurisdictie-herkenning | Correct rechtsgebied | 98% |
| Onzekerheidskalibratie | Betrouwbaarheidsintervallen | 0.80 |
| Consistentie | Herhaalbaarheid bij variaties | 90% |
| Robuustheid | Promptvariatie-bestendigheid | 85% |
| Privacy | Geen PII-lekken | 100% |
| Bias | Geen systematische voorkeuren | 90% |

### 3.2 Subgroeprapportage

Geen totaalscore zonder uitsplitsing naar:
- Rechtsgebied (strafrecht, civielrecht, bestuursrecht, etc.)
- Taaktype (samenvatten, analyseren, adviseren, etc.)
- Fouttype (9 types)
- Severity (S1-S5)

## 4. Severity-weighted Scoring

### 3.1 Severity Levels

| Level | Impact | Weight | Release Gate |
|-------|--------|--------|--------------|
| S1 Cosmetisch | Geen extern gevolg | 1 | Geen blokkade |
| S2 Herstelbaar | Intern herstelbaar | 2 | Warning |
| S3 Materieel | Inhoudelijke fout | 4 | Blokkade |
| S4 Rechtsverlies | Potentieel rechtsverlies | 8 | Hard block |
| S5 Systeemisch | Ernstige/systemische schade | 16 | Hard block + incident |

### 3.2 Acceptatie-formule

```
Acceptatie = (Verwachte_waarde × Detecteerbaarheid × Herstelbaarheid × Schaal)
             > (Ernst_component × Schaal)
```

Een systeem met veel S1-fouten kan acceptabeler zijn dan een systeem met één terugkerende S5-fout.

## 5. Evidence Lineage

Elk materieel antwoord moet herleidbaar zijn tot:

1. Model- en systeemversie
2. Prompt-template
3. Gebruikte tools
4. Geraadpleegde bronnen
5. Bronversies en geldigheidsdatum
6. Retrievalresultaten
7. Gegenereerd antwoord
8. Menselijke wijzigingen
9. Uiteindelijke beslissing

Model-gegenereerde uitleg is **geen** betrouwbare audit trail.

## 6. Continue Evaluatie (CI/CD/CT)

### 6.1 Testpiramide

```
         /\
        /  \     Adversarial tests (maandelijks)
       /────\
      /      \   Challenge set (kwartaal)
     /────────\
    /          \ Regression set (elke commit)
   /────────────\
  /              \ Unit tests (elke commit)
 /────────────────\
```

### 6.2 Triggers voor Evaluatie

- Elke code-commit (regression)
- Model-wijziging (volledige suite)
- Prompt-wijziging (regression + challenge)
- Bron-index update (retrieval tests)
- Productie-incident (incident-driven tests)
- Regelgeving-wijziging (domain review)

## 7. Benchmark Capture Prevention

### 7.1 Risico's

| Risico | Beschrijving | Mitigatie |
|--------|--------------|-----------|
| Benchmark capture | Vendor beïnvloedt benchmark | Onafhankelijke testdata |
| Teaching to the test | Optimalisatie op bekende tests | Verborgen challenge-set |
| Metric laundering | Hoge totaalscore verbergt zwaktes | Subgroeprapportage verplicht |
| Access asymmetry | Grote partijen testen beter | Open-source baseline |
| Temporal decay | Verouderde resultaten | 90-dagen expiry |

### 7.2 Canary Mechanism

Canary tokens in de challenge set detecteren of testdata in training is gebruikt. Tokens worden extern beheerd (`.benchmark-canary`) om false positives te voorkomen.

## 8. EU AI Act Alignment

| Artikel | Eis | JLAIF Implementatie |
|---------|-----|---------------------|
| Art. 12 | Logging/record-keeping | Evidence lineage + Gate receipts |
| Art. 13 | Transparantie | Model card + subgroeprapportage |
| Art. 15 | Accuracy/robustness | Regression + challenge + drift gates |
| Art. 62-63 | Post-market monitoring | Drift monitor + incident-driven tests |

## 9. CEPEJ Alignment

| Principe | JLAIF Implementatie |
|----------|---------------------|
| Legal certainty | Severity-weighted scoring + release gates |
| Judicial independence | Human review required for L3+ |
| Human oversight | `human_review_required` in EvidenceLineage |
| Transparency | Evidence lineage + model card |
| Traceability | Gate receipts + lineage hashing |

## 10. Referentiemodule-index

| Module | Pad | Functie |
|--------|-----|---------|
| Error Taxonomy | `api/assurance/error_taxonomy.py` | 9 fouttypes + S1-S5 severity |
| Severity Scorer | `api/assurance/severity_scorer.py` | Stanford acceptability formula |
| Release Gate | `api/assurance/release_gate.py` | GO/NO-GO/CONDITIONAL |
| Codebase Scanner | `api/assurance/scanner.py` | Pattern-based compliance detection |
| Regression Set | `api/assurance/regression_set.py` | 12+ regression cases |
| Challenge Set | `api/assurance/challenge_set.py` | 10+ challenge cases + canary |
| Drift Monitor | `api/assurance/drift_monitor.py` | Performance drift detection |
| Incident Tests | `api/assurance/incident_driven_tests.py` | Incident → test generation |
| Temporal Decay | `api/assurance/temporal_decay.py` | 90-day expiry |
| Djimitflo Bridge | `api/assurance/djimitflo_bridge.py` | Compliance task generation |
| Benchmark Capture | `api/assurance/benchmark_capture_prevention.py` | Canary mechanisme |
| Evidence Lineage | `shared/gate/lineage.py` | CEPEJ JAI-06 traceability |
| CI Gates | `api/ci_gates.py` | Regression + challenge + drift gates |
| CI Workflow | `.github/workflows/jlaif-assurance.yml` | GitHub Actions pipeline |
