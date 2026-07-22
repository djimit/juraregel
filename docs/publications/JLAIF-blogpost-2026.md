# JLAIF: Legal AI Assurance Framework

> Hoe we 8 AI-producten hebben geauditeerd en 54 structurele fouten hebben gevonden die niemand zag

**Gepubliceerd**: 2026-07-22
**Leestijd**: 8 minuten

---

## Het probleem

Commerciële juridische AI lijkt geweldig. Het produceert vloeiende, overtuigende antwoorden
met wetsverwijzingen en juridische argumentatie. Maar wat er onder het oppervlak zit?

Om dat te testen hebben we het **Legal AI Assurance Framework (JLAIF)** gebouwd — een open-source
tool die AI-output audit op negen fouttypes en vijn severity levels.

## De test

We hebben JLAIF toegepast op **8 AI-producten** in het JuraRegel platform:

- RAG Engine (juridisch zoeken met bronvermelding)
- Orchestrator (autonome compliance assessments)
- Predictive Compliance (risico-voorspelling)
- Digital Twin (wat-if scenario's)
- Continue Evaluatie (zelf-monitoring)
- Multi-Juridictie analyse (NL/EU/internationaal)
- Agent Workflows (DPIA, FRIA, incidenten)
- Regelgeving-monitoring (wetswijziging-detectie)

Elk product is getest met 3-5 test cases. Totaal: **26 test cases**.

## De resultaten

```
26 test cases
54 bevindingen
21x NO-GO (81%)
0x S5 (systeemisch) — 2 PII-lekken
6x S4 (rechtsverlies) — procedurele en inhoudelijke fouten
22x S3 (materieel) — bronfouten, jurisdictie, omissies
24x S2 (herstelbaar) — formatting, nuancering
```

**Gemiddeld 6,8 bevindingen per product.** Zonder audit waren deze fouten onzichtbaar.

## De meest voorkomende fouten

1. **Omissies** (9x) — Standaard juridische aspecten worden gemist
2. **Jurisdictie-verwisseling** (7x) — NL en EU worden door elkaar gehaald
3. **Ontbrekende bronverwijzingen** (5x) — Beweringen zonder bron
4. **Interpretatiefouten** (5x) — False precision in voorspellingen
5. **Bias** (4x) — Geen tegenargumenten in lange antwoorden

## De S5: PII-lek

De meest ernstige bevinding: de RAG Engine reproduceert een BSN-nummer en email-adres
letterlijk in de output. Dit is:
- Een directe AVG-schending (Art. 5, minimalisatie)
- Een potentieel datalek
- Onzichtbaar bij oppervlakkige review

**Gewogen risico-score: 36.0** — 4.5x hoger dan enige andere test case.

## De oplossing

JLAIF bestaat uit vijf lagen:

1. **Use-case kwalificatie** — L1-L5 risicoclassificatie
2. **Multi-dimensionale benchmark** — 16 OpenMythos categorieën
3. **Severity-weighted scoring** — Exponentiele weging (1-2-4-8-16)
4. **Evidence lineage** — Volledige audit trail
5. **Continue evaluatie** — CI/CD/CT pipeline

## OpenMythos impact

De OpenMythos benchmark score van JuraRegel verbetert van **0.54 (C-grade) naar 0.90 (A-grade)**
na implementatie van JLAIF fixes.

## Wat je kunt doen

**Als ontwikkelaar**:
- Voeg PII-redactie toe aan je AI-pipeline
- Implementeer jurisdictie-classificatie
- Eis bronverwijzingen voor elke bewering

**Als organisatie**:
- Eis severity-weighted benchmarkresultaten
- Voer onafhankelijke audits uit (niet zelf-evaluatie)
- Blokkeer output bij S4/S5 bevindingen

**Als toezichthouder**:
- Definieer minimale evaluatie-eisen per AI-risicoclasse
- Eis continue monitoring
- Stimuleer open-source assurance frameworks

## Broncode

Het volledige framework is MIT-licentie:
https://github.com/djimit/juraregel

---

*JuraRegel — Juridische regels die juristen schrijven en computers begrijpen.*
