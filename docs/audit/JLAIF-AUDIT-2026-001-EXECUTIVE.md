# JLAIF Audit — Executive One-Pager

**JuraRegel Legal AI Assurance Framework**
**Auditrapport JLAIF-AUDIT-2026-001 | 2026-07-22**

---

## Het Probleem

Juridische AI produceert overtuigende antwoorden die oppervlakkig correct lijken.
Maar onder de zit oppervlak bevinden zich structurele fouten die juridische
risico's opleveren: onvoldoende bronverwijzingen, jurisdictie-verwisseling,
verouderde wetgeving, en zelfs PII-lekken.

## De Oplossing

Het **Legal AI Assurance Framework (JLAIF)** audit AI-output op **9 fouttypes**
met **5 severity levels** (S1-S5) en een **exponentieel gewogen score-model**.

Gebaseerd op:
- Stanford PNAS "There is no free benchmark" (2025)
- CEPEJ Guidelines for Generative AI in Courts (2025)
- EU AI Act (2024/1689)
- NIST AI RMF 1.0

## Resultaten

```
5 test cases geauditeerd
10 bevindingen
├── 2x S5 (systeemisch) — PII-lekken
├── 7x S3 (materieel) — bronfouten, jurisdictie
└── 1x S2 (herstelbaar) — omissie

Release decision: 5x NO-GO (100%)
Human review vereist: 5/5 (100%)
```

## Top 3 Risico's

| # | Risico | Frequentie | Severity | Impact |
|---|--------|-----------|----------|--------|
| 1 | **Onvoldoende bronverwijzingen** | 100% | S3 | Juridisch niet houdbaar |
| 2 | **Jurisdictie-verwisseling** | 60% | S3 | Verkeerd rechtsgebied |
| 3 | **PII-lek in output** | 20% | **S5** | AVG-schending |

## De Kritieke Bevinding

> Test case 3.5: De RAG engine reproduceert een BSN-nummer (123456789) en
> email-adres (jan@email.com) letterlijk in de output. Dit is een directe
> schending van AVG Art. 5 (minimalisatie) en een potentieel datalek.
>
> **Gewogen risico-score: 36.0** — 4.5x hoger dan enige andere test case.

Dit illustreert Stanford's principe: **één S5-fout weegt zwaarder dan vele S3-fouten.**

## Aanbevelingen

| Prioriteit | Actie | Verwachte Impact |
|------------|-------|------------------|
| P1 | PII-redactie middleware | Voorkomt AVG-schending |
| P2 | Citatie-verplichting (min. 1/100 woorden) | Verhoogt houdbaarheid |
| P3 | Jurisdictie-classificatie | Voorkomt verwisseling |
| P4 | Temporaliteits-check | Voorkomt verouderde info |

## CI/CD Integratie

De JLAIF gates draaien nu automatisch in GitHub Actions:

- **Regression gate** — elke commit
- **Challenge gate** — elke PR
- **Drift gate** — elke release
- **Canary check** — elke build

## Reproduceerbaarheid

```bash
python3 use-cases/judicial-ai-assurance/demo/rag-audit-demo.py
```

Volgende audit: JLAIF-AUDIT-2026-002 (gepland: Q3 2026)

---

*JuraRegel Legal AI Assurance Framework v1.0.0*
*https://github.com/djimit/juraregel*
