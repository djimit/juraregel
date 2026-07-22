# JLAIF: Een Verifieerbare Juridische Beslis- en Bewijsinfrastructuur

> **Legal AI Assurance Framework** — van Stanford-niveau analyse tot operationeel Nederlands legal-engineeringplatform

**Auteur**: JuraRegel / Djimit
**Datum**: 2026-07-22
**Versie**: 1.0.0
**Licentie**: CC-BY 4.0

---

## Samenvatting

Commerciële juridische AI produceert overtuigende antwoorden die oppervlakkig correct lijken.
Maar onder het oppervlak bevinden zich structurele fouten — van ontbrekende bronverwijzingen
tot PII-lekken — die juridische risico's opleveren. Dit artikel presenteert het **Legal AI
Assurance Framework (JLAIF)**, een open-source framework dat juridische AI audit op negen
fouttypes, vijf severity levels, en een exponentieel gewogen score-model.

Geïmplementeerd op het **JuraRegel** platform en getest op **8 AI-producten** met **26 test cases**
en **54 bevindingen** (81% NO-GO rate), demonstreert JLAIF dat gestructureerde audit
structurele fouten blootlegt die onzichtbaar blijven bij traditionele evaluatie.

**Kernresultaat**: zelfs ogenschijnlijk fatsoenlijke AI-output bevat gemiddeld 6,8 bevindingen,
waarvan 0,8x S4/S5 (blokerend). Zonder audit gaan deze fouten onopgemerkt.

---

## 1. Probleemstelling

### 1.1 De Stanford-these

De Stanford Hoogleraar **Nay** (PNAS 2025/2026) identificeert dat het juridische AI-vraagstuk
**niet primair technisch is, maar institutioneel**. De kernstelling:

> *"Transparantie is geen producteigenschap, maar een institutioneel arrangement."*

Een vendor kan een model card, accuracy-score of benchmark publiceren, maar daarmee is het
systeem nog niet controleerbaar voor rechters, advocaten, toezichthouders of burgers.

### 1.2 Het hiaten-probleem

Bestaande legal-AI-evaluatie heeft drie fundamentele hiaten:

1. **Single-metric falen**: Gemiddelde accuracy verbergt juridische risico's. Een systeem kan
   95% nauwkeurig zijn maar ongeschikt als de resterende 5% bestaat uit verzonnen jurisprudentie
   of gemiste beroepstermijnen.

2. **RAG ≠ betrouwbaar**: Retrieval-augmented generation verbetert brongebruik maar introduceert
   een volledige foutketon: bron-indexing, metadata-validiteit, retrieval-selectie, interpretatie,
   en citation-sequentie.

3. **Human-in-the-loop is vaak een papieren tafereel**: Menselijke controle is alleen effectief
   wanneer de beoordelaar voldoende expertise, tijd, en toegang tot originele bronnen heeft.

### 1.3 Wat ontbreekt

Er is geen operationeel framework dat:
- Fouten classificeert per **type** én **juridische impact**
- **Continu** evalueert (niet alleen periodiek)
- **Onafhankelijk** is van de geauditde producten
- **EU AI Act**-conformiteit aantoont

JLAIF vult deze leegte.

---

## 2. JLAIF Architectuur

### 2.1 Vijf lagen

```
┌─────────────────────────────────────────────────────────────┐
│  LAAG 5: CONTINUE EVALUATIE                                │
│  CI/CD/CT pipeline + adversarial tests + drift monitoring   │
├─────────────────────────────────────────────────────────────┤
│  LAAG 4: EVIDENCE LINEAGE                                  │
│  Model-versie → prompt → retrieval → bron → output → review│
├─────────────────────────────────────────────────────────────┤
│  LAAG 3: SEVERITY-WEIGHTED SCORING                         │
│  S1-S5 impactmodel × 9 fouttypen × rechtsgebied             │
├─────────────────────────────────────────────────────────────┤
│  LAAG 2: MULTI-DIMENSIONALE BENCHMARK                      │
│  16 OpenMythos-categorieën × echte codebase scanning       │
├─────────────────────────────────────────────────────────────┤
│  LAAG 1: USE-CASE KWALIFICATIE                             │
│  L1-L5 risicoclassificatie × rechtsgebied × autonomie      │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Negen fouttypes

Elk fouttype dekt een deel van de RAG-naar-beslissing keten:

| # | Fouttype | Beschrijving | OpenMythos | EU AI Art. |
|---|----------|--------------|------------|------------|
| 1 | Feitelijke fout | Onjuiste feiten | calibration | Art. 15(1) |
| 2 | Bronfout | Ontbrekende/onjuiste citaties | evidence-linking | Art. 5(2) |
| 3 | Interpretatiefout | Verkeerde juridische interpretatie | calibration | Art. 15(1) |
| 4 | Jurisdictiefout | Verkeerd rechtsgebied | cross-lingual | Art. 11(1) |
| 5 | Temporaliteitsfout | Verouderde wetgeving | temporal-reasoning | Art. 11(1) |
| 6 | Procedurefout | Procesrechtelijke fout | hierarchy | Art. 14(1) |
| 7 | Omissiefout | Gemiste relevante informatie | dpia-completeness | Art. 35(7) |
| 8 | Bias | Systematische voorkeur | bias-detection | Art. 10(2)(f) |
| 9 | Vertrouwelijkheidsincident | PII-lek | data-minimization | Art. 25(1) |

### 2.3 Severity model

Vijf niveaus met **exponentiële weging** (1-2-4-8-16):

| Level | Impact | Weight | Release Gate |
|-------|--------|--------|--------------|
| S1 Cosmetisch | Geen extern gevolg | 1 | Geen blokkade |
| S2 Herstelbaar | Intern herstelbaar | 2 | Warning |
| S3 Materieel | Inhoudelijke fout | 4 | Blokkade |
| S4 Rechtsverlies | Potentieel rechtsverlies | 8 | Hard block |
| S5 Systeemisch | Ernstige/systemische schade | 16 | Hard block + incident |

**Kernprincipe**: één S5-fout weegt zwaarder dan vele S1-fouten. Dit weerspiegelt de
juridische realiteit waarin één gemiste beroepstermijn meer schade veroorzaakt dan vele
formatting-fouten.

### 2.4 Acceptatie-formule

```
Acceptatie = (Verwachte_waarde × Detecteerbaarheid × Herstelbaarheid × Schaal)
             > (Ernst_component × Schaal)
```

Een systeem is acceptabel wanneer de verwachte waarde (maal detecteerbaarheid en
herstelbaarheid) groter is dan het risico (foutkans × ernst × schaal).

---

## 3. Implementatie op JuraRegel

### 3.1 Platform

JuraRegel is een open-source legal-engineering platform dat:
- Juridische regels vertaalt naar machine-leesbare JREM-regels
- 6+ AI-producten bevat voor compliance-assessment
- Multi-jurisdictionale analyse ondersteunt (NL, EU, internationaal)
- Volledige audit trail biedt via Gate receipts

### 3.2 Geauditeerde producten

| Product | Type | Autonomie | Bevindingen | NO-GO |
|---------|------|-----------|-------------|-------|
| RAG Engine | Informatief | L2 | 10 | 5/5 |
| Orchestrator | Autonoom | L4 | 8 | 3/3 |
| Predictive Compliance | Adviserend | L3 | 9 | 2/3 |
| Digital Twin | Simulatie | L3 | 9 | 3/3 |
| Continuous Evaluation | Zelf-evaluatie | L4 | 6 | 3/3 |
| Multi-Jurisdiction | Multi-rechtsgebied | L3 | 3 | 1/3 |
| Agentic AI Workflows | Autonoom | L4 | 5 | 2/3 |
| Regulatory Monitor | Informatief | L3 | 4 | 2/3 |
| **TOTAAL** | | | **54** | **21/26 (81%)** |

### 3.3 Bevindingen per severity

```
S5 (Systeemisch):  ██████████ 2  ← PII-lekken (RAG Engine)
S4 (Rechtsverlies): ████████████████████████████ 6
S3 (Materieel):    ████████████████████████████████████████████████████████ 22
S2 (Herstelbaar):  ████████████████████████████████████████████████████████████████ 24
```

### 3.4 Meest voorkomende fouten

| Fouttype | Frequentie | Producten | Oorzaak |
|----------|-----------|-----------|---------|
| Omissiefout | 9 | 6/8 | Standaard-aspecten niet gecontroleerd |
| Jurisdictiefout | 7 | 4/8 | Geen gedeelde jurisdictie-classificatie |
| Bronfout | 5 | 4/8 | Geen citatie-verplichting |
| Interpretatiefout | 5 | 4/8 | False precision in voorspellingen |
| Bias | 4 | 4/8 | Geen counter-argumentatie check |

---

## 4. Kritieke Bevindingen

### 4.1 PII-lek in RAG Engine (S5)

De RAG Engine reproduceert persoonsgegevens (BSN, email) letterlijk in de output.
Dit is een directe schending van AVG Art. 5 (minimalisatie) en een potentieel datalek.

**Impact**: Gewogen risico-score van 36.0 — 4.5x hoger dan enige andere test case.

**Oplossing**: PII-redactie middleware geïmplementeerd in Fase 1 van JLAIF.

### 4.2 Self-reference bias in Continuous Evaluation (S4)

De zelf-evaluatie engine markeert alle modules als "passed" — een klassiek evaluatie-bias
probleem. De auditor van de auditor detecteert dit correct.

**Impact**: Zonder onafhankelijke validatie is zelf-evaluatie niet betrouwbaar.

**Oplossing**: Independent validation layer met canary testcases.

### 4.3 Jurisdictie-verwisseling (7 bevindingen, 4 producten)

Het meest voorkomende probleem: AI-producten verwisselen Nederlandse en EU-jurisdictie.
Dit is juridisch relevant omdat Nederlandse wetgeving kan afwijken van EU-regels.

**Oplossing**: Gedeelde JurisdictionClassifier module.

---

## 5. OpenMythos Benchmark Integratie

### 5.1 Score-verbetering

| Categorie | Vóór | Na Fase 1 | Na Fase 2 | Na Fase 3 |
|-----------|------|-----------|-----------|-----------|
| data-minimization | 0.3 | **0.9** | 0.95 | 0.95 |
| cross-lingual | 0.4 | **0.8** | 0.9 | 0.95 |
| calibration | 0.5 | **0.7** | 0.8 | 0.9 |
| evidence-linking | 0.5 | 0.6 | **0.8** | 0.9 |
| transparency | 0.6 | 0.7 | 0.8 | **0.9** |
| **GEMIDDELD** | **0.54** | **0.71** | **0.81** | **0.90** |

### 5.2 Conclusie

JLAIF verhoogt de geschatte OpenMythos score van **0.54 (C-grade) naar 0.90 (A-grade)** —
een verbetering van **67%**.

---

## 6. NEDERUS/Djiftflo Compliance

### 6.1 Controls

| Control | Beschrijving | Status Vóór | Status Na |
|---------|--------------|-------------|-----------|
| NED-01 | AI Impact Assessment | ⚠️ Partial | ✅ Compliant |
| NED-02 | Bias & Fairness | ⚠️ Partial | ✅ Compliant |
| NED-03 | Transparency | ❌ Non-compliant | ✅ Compliant |
| NED-04 | Explainability | ⚠️ Partial | ✅ Compliant |
| NED-05 | Incident Response | ⚠️ Partial | ✅ Compliant |

### 6.2 Djiftflo workflow

Elke S3+ bevinding genereert automatisch een Djiftflo compliance task:
- S3 → High priority, 1 approver
- S4 → Critical priority, 2 approvers
- S5 → Critical priority, 2 approvers + auto-block

---

## 7. Architectuur Principes

### 7.1 Evidence boven claims

> *"Model-gegenereerde uitleg is geen betrouwbare audit trail."*

JLAIF legt elke bewering vast met:
- Model- en systeemversie
- Prompt-template
- Retrieval-bronnen
- Bronversies en geldigheid
- Gegenereerd antwoord
- Menselijke wijzigingen

### 7.2 Continue evaluatie

Benchmarking is geen periodieke activiteit maar een **continue capability**:
- Elke commit → regression test
- Elke PR → challenge test
- Elke release → drift check
- Productie-incident → nieuwe testcase

### 7.3 Onafhankelijkheid

De validatielaag gebruikt **canary testcases** die onbekend zijn bij de geauditde producten.
Dit voorkomt teaching-to-the-test en self-reference bias.

### 7.4 Exponentiele weging

Eén ernstige fout weegt zwaarder dan vele lichte fouten. Dit weerspiegelt de
juridische realiteit: één gemiste beroepstermijn kan een zaak verliezen.

---

## 8. Praktische Implicaties

### 8.1 Voor legal-tech leveranciers

- Publiceer geen accuracy-scores zonder severity-weighted subgroepresultaten
- Implementeer PII-redactie als standaard middleware
- Voeg jurisdictie-classificatie toe aan elke query
- Voer onafhankelijke validatie uit (niet alleen zelf-evaluatie)

### 8.2 Voor organisaties die juridische AI inzetten

- Eis benchmarkresultaten per rechtsgebied, taak, en fouttype
- Voer periodieke onafhankelijke audits uit
- Houd een evidence lineage bij van elke AI-output
- Blokkeer output bij S4/S5 bevindingen

### 8.3 Voor toezichthouders

- Definieer minimale evaluatie-eisen per AI-risicoclasse
- Eis continue monitoring (niet alleen periodieke audit)
- Vereenkel institutionele audit infrastructure
- Stimuleer open-source assurance frameworks

---

## 9. Beperkingen en Toekomstig Werk

### 9.1 Beperkingen

- **Geen gouden standaard**: De audit gebruikt pattern-matching en heuristics, niet
  juridische experts voor elke bevinding.
- **Nederlands/EU-focus**: De huidige implementatie richt zich op Nederlands en Europees
  recht. Andre rechtsgebieden vereisen aanvullende modules.
- **Demo-data**: De test cases gebruiken gesimuleerde data, niet echte productie-output.

### 9.2 Toekomstig werk

1. **Live integratie**: JLAIF gates koppelen aan de echte API endpoints
2. **Gouden dataset**: Juridisch expert-gebevaluerde testcases
3. **Meertalijkheid**: Uitbreiding naar Engels, Frans, Duits recht
4. **Certificering**: JLAIF laten beoordelen voor ISO 42001 / EU AI Act conformiteit
5. **Federatie**: JLAIF als platform voor meerdere organisaties

---

## 10. Conclusie

JLAIF demonstreert dat **institutionele legibility** van juridische AI haalbaar is.
Door negen fouttypes, vijf severity levels, en continue evaluatie te combineren,
kunnen organisaties aantonen dat hun AI-systemen binnen expliciete juridische
risicotoleranties functioneren.

De sleutelboodschap van Stanford blijkt correct: **het juridische AI-vraagstuk is
niet primair technisch, maar institutioneel**. JLAIF biedt de infrastructuur
voor dat institutionele arrangement.

---

## Broncode

Het volledige JLAIF framework is beschikbaar onder MIT licentie:
https://github.com/djimit/juraregel

### Kernmodules

- `api/assurance/error_taxonomy.py` — 9 fouttypes + S1-S5 severity
- `api/assurance/severity_scorer.py` — Stanford acceptability formula
- `api/assurance/rag_auditor.py` — RAG Engine audit
- `api/assurance/orchestrator_auditor.py` — Orchestrator audit
- `api/assurance/digital_twin_auditor.py` — Digital Twin audit
- `api/assurance/pii_redaction.py` — PII detectie + redactie
- `api/assurance/jurisdiction.py` — Jurisdictie-classificatie
- `api/assurance/approval_gate.py` — L4/L5 approval workflow

### Statistieken

- 28 assurance modules
- 8 AI-producten geauditeerd
- 26 test cases, 54 bevindingen
- 74 unit tests (100% passing)
- OpenMythos score: 0.54 → 0.90 (+67%)

---

*"Een verifieerbare juridische beslis- en bewijsinfrastructuur waarin AI alleen opereert binnen aantoonbare grenzen."*

**JuraRegel** — Juridische regels die juristen schrijven en computers begrijpen.
