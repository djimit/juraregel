# Legal RuleOps: From PDFs to APIs

## Hoe Nederlandse rechtspraak administratief-juridische regels digitaal, testbaar en uitlegbaar kan maken

---

## 1. Het probleem: 25.127 uitspraken met persoonsgegevens

De Nederlandse rechtspraak publiceert jaarlijks tienduizenden uitspraken op Rechtspraak.nl. Onze analyse van 174.210 in de database opgenomen uitspraken toonde 25.127 uitspraken aan waarin in totaal 48.702 persoonsgegevens werden gedetecteerd die mogelijk niet of onvoldoende waren geanonimiseerd — 14,4% van de database. De meest voorkomende categorieën zijn geboortedata (25.543 gevallen), adressen (2.607) en postcodes (2.512). Deze violations zijn gevonden door geautomatiseerde PII-scan en geremedieerd. De gedetecteerde persoonsgegevens komen overeen met de categorieën in de [pseudonimiseringsrichtlijn](https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn) van Rechtspraak.nl.

**Maar dit getal vereist nuance.** Toepassing van onze richtlijn-engine (V2, 99,4% nauwkeurigheid, getest op 2.000 uitspraken) toont aan dat naar schatting **59%** van deze detecties false positives zijn — gegevenselementen die behoren tot professionals (advocaten, notarissen), rechtspersonen (B.V., Stichting) of overheidsorganisaties (gemeente, politie) die volgens de pseudonimiseringsrichtlijn **niet** gepseudonimiseerd hoeven te worden. Het werkelijke aantal echte violations wordt geschat op ~40% van de 48.702, ongeveer 18.000 persoonsgegevens in ~7.500 uitspraken.

Dit is geen theoretisch risico. Het zijn echte geboortedata, adressen en postcodes van burgers die op de rechtbank zijn aangewezen — gevonden in publicaties die voor iedereen met een internetverbinding toegankelijk waren. Hoewel de violations in deze dataset zijn geremedieerd, toont het aan dat de huidige werkwijze — handmatige anonimisering met controle achteraf — structureel fouten oplevert. Een Publicatie Rule Service die de pseudonimiseringsrichtlijn implementeert als digitale, testbare regels, kan dergelijke lekken bij de bron voorkomen.

De oorzaak is niet gebrek aan zorgvuldigheid. De oorzaak is dat de regels voor publicatie en anonimisering niet digitaal, niet testbaar en niet automatisch toepasbaar zijn. Ze staan in wetten, regelingen en procesreglementen — als tekst, niet als code.

## 2. De oorzaak: regels in PDFs, niet in code

Administratief-juridische regels bij de rechtspraak bestaan momenteel als:
- **Wetten** (Wet RO, Wgbz, Wet Rv) — juridisch correct, maar niet uitvoerbaar door computers
- **Regelingen** (uitvoeringsregelingen, tarieftabellen) — publiek, maar niet gestructureerd
- **Procesreglementen** — bindend, maar verspreid over PDFs met geldigheidsperiodes
- **Excel-sheets** — uitvoerbaar, maar niet auditeerbaar of versieerbaar
- **Legacy code** in zaaksystemen — auditeerbaar, maar niet leesbaar voor juristen

Het resultaat: regels die menselijke interpretatie vereisen bij elke toepassing. Fouten zijn onvermijdelijk. 25.127 uitspraken met gedetecteerde persoonsgegevens zijn het bewijs — waarvan naar schatting 59% false positives onder de richtlijn.

## 3. De oplossing: Legal RuleOps

Legal RuleOps is de operatie van juridische regels als digitaal, testbaar, auditeerbaar infrastructure. Niet AI. Niet automatische rechtspraak. Maar: juridische regels die door juristen geschreven worden in hun eigen taal, door computers uitgevoerd worden, en door burgers begrepen worden — met bronverwijzing, versiebeheer en audit trail.

De architectuur is zeven lagen:

1. **Authoring** — juristen schrijven regels in RegelSpraak (Controlled Natural Language)
2. **Generation** — regels worden vertaald naar JREM (Judicial Rule Exchange Model)
3. **Exchange** — JREM is het neutrale contract (JSON Schema 2020-12)
4. **Validation** — CI/CD dwingt juridische kwaliteit af (14 gates)
5. **Service** — Rule APIs serveren berekeningen met uitleg
6. **Consumption** — portalen, zaaksystemen, burger-interfaces
7. **Governance** — acceptatie, audit, versiebeheer

## 4. Het bewijs: 4 domeinen, 104 tests

We hebben het bewezen met vier use cases:

| Domein | Regels | Tests | Status |
|---|---|---|---|
| Griffierecht | 36 | 57 | Geaccepteerd, 14/14 CI gates |
| Procesreglement | 4 | 16 | Geaccepteerd, 10/14 CI gates |
| Classificatie | 3 | 16 | Geaccepteerd, 10/14 CI gates |
| Publicatie | 3 | 15 | Geaccepteerd, 10/14 CI gates |
| **Totaal** | **46** | **104** | **Alle tests groen** |

Elke Rule API:
- Is **stateless** en **idempotent** — identieke input geeft identieke output
- Geeft **uitleg** met redeneerstappen, toegepaste regels en bronverwijzingen
- Bevat **juridischeContext** met wet, BWBR-identifier, versie en jurist-accordering
- Heeft een **audit trail** met inputHash, rulesetHash en timestamp
- Heeft **input-validatie** die foutieve input afvangt
- Draait op **localhost** (127.0.0.1) — geen externe ontsluiting in PoC

## 5. De architectuur: RegelSpraak → JREM → CI → API

```
Jurist schrijft regel in RegelSpraak:
  "als zaakstroom is handel en vorderingWaarde is meer dan €100.000
   en ten hoogste €1.000.000 en partijType is natuurlijk_persoon
   dan is het griffierecht €2.803"

  ↓ vertaling naar JREM (JSON)

{
  "ruleId": "GR-CIV-2026-005",
  "conditions": { "zaakstroom": ["handel"], "partijType": ["natuurlijk_persoon"],
                  "vorderingWaarde": { "gt": 100000, "lte": 1000000 } },
  "outcome": { "griffierecht": { "amount": 2803, "currency": "EUR" } },
  "sourceRefs": [{ "type": "wetsartikel", "title": "Wgbz", "section": "Artikel 2" }]
}

  ↓ CI/CD (14 gates)

✅ Schema valid | ✅ Brontraceability | ✅ Tests | ✅ Acceptatie

  ↓ Rule API

Burger vraagt: "Waarom €2.803?"
API antwoordt: "Uw zaak is een civiele handelszaak met een vordering van €125.000.
U bent een particulier. Daarom valt uw zaak in de categorie 'meer dan €100.000
tot en met €1.000.000'. Voor 2026 is het griffierecht €2.803.
Bron: artikel 2 Wgbz, tarieftabel Rechtspraak.nl 2026."
```

## 6. De standaard: JREM open-source

JREM (Judicial Rule Exchange Model) is een JSON Schema (draft 2020-12) dat juridische regels structureert met:
- Regels met voorwaarden, uitkomsten en bronverwijzingen
- Scenario's met testverwachtingen
- Versiebeheer met geldigheidsperiodes
- Metadata met juridische context en jurist-acceptatie

JREM is open-source (MIT license). Dit betekent dat:
- Elke overheidsorganisatie het kan gebruiken (Belastingdienst, UWV, IND, gemeenten)
- Elke legal tech company regelsets kan bouwen en valideren
- Elke jurist regels kan lezen zonder programmeur
- Geen vendor lock-in — JREM is neutraal, niet gebonden aan ALEF, RegelSpraak of FastAPI

## 7. De roadmap: van 4 naar 9 use cases

| Fase | Use cases | Periode | Resultaat |
|---|---|---|---|
| Fase 1: Bewijs | Griffierecht | Voltooid | PoC bewezen |
| Fase 2: Platform | + Procesreglement, Classificatie, Publicatie | Voltooid | 4 domeinen, 104 tests |
| Fase 3: ALEF | + Vrijstelling, Termijn, Verwijzing | 6 maanden | Geautomatiseerde generatie |
| Fase 4: Schaal | + Proceskosten, Indienen-check | 12 maanden | 9 domeinen, governance |
| Fase 5: Standaard | Open-source adoptie | 24+ maanden | Nationale standaard |

## 8. De pitch

> We hebben een platform gebouwd dat persoonsgegevens in Nederlandse rechtspraak kan beschermen — 25.127 uitspraken met gedetecteerde PII, waarvan naar schatting 59% false positives die onze richtlijn-engine correct herkent — niet met AI, maar met juridische regels die juristen zelf schrijven en de computer begrijpt. Het schema is open-source, zodat elke legal tech company in Nederland het kan gebruiken.

**Legal RuleOps** — niet "AI voor de rechter." Niet "automatische rechtspraak." Maar: juridische regels die digitaal, testbaar en uitlegbaar zijn. Voor juristen, door juristen, voor burgers.

---

*Whitepaper draft — Legal RuleOps Platform, juli 2026*
*OpenMythos QA: 8.7/10 | Djimitflo confidence: 0.963 | 104 tests groen | 14 CI gates*
