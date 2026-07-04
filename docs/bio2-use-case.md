# BIO2 Use Case — Baseline Informatiebeveiliging Overheid

## Overzicht

De BIO2 use case voegt de Baseline Informatiebeveiliging Overheid toe als vijfde use case in JuraRegel. Met 162 overheidsmaatregelen (uit 167 totaal, 5 zijn ISO-only) gebaseerd op ISO 27001/27002, bewijst deze use case dat JuraRegel schaalt voorbij de Rechtspraak naar de hele overheid.

## Architectuur

```
MinBZK GitHub (167 maatregelen in Markdown)
  ↓ bio2_parser.py — gh api → base64 decode → parse ### headers
162 overheidsmaatregelen met maatregelId, categorie, ISO ref
  ↓ RegelSpraak CNL — 162 regels
  ↓ JREM export — bio2-maatregelen-2025.1.json
  ↓ Rule API — create_app("bio2", jrem_path, 8494)
POST /v1/bio2/calculate — check maatregel compliance
GET /v1/bio2/maatregelen — lijst alle maatregelen
GET /v1/bio2/rapport/{orgId} — ENSIA-gealigned compliance rapport
```

## API Endpoints

| Endpoint | Methode | Functie |
|---|---|---|
| /v1/health | GET | Healthcheck met ruleset info |
| /v1/bio2/calculate | POST | Check maatregel compliance (via factory) |
| /v1/bio2/maatregelen | GET | Lijst alle 162 maatregelen met ISO ref |
| /v1/bio2/rapport/{orgId} | GET | Compliance rapport per organisatie (ENSIA aligned) |
| /v1/bio2/versions | GET | Beschikbare BIO2 versies |
| /v1/rules/{ruleId} | GET | Regel metadata met ISO referentie |
| /v1/audit/{calcId} | GET | Audit trail |

## Maatregelen per categorie

| Categorie | Aantal | ISO 27002 ref |
|---|---|---|
| Organisatorisch | 72 | 5.x |
| Technologisch | 66 | 8.x |
| Fysiek | 17 | 7.x |
| Mensgericht | 12 | 6.x |
| **Totaal** | **162** (167 minus 5 ISO-only) | |

## Compliance Rapport

`GET /v1/bio2/rapport/gemeente-amsterdam` retourneert:

```json
{
  "organisatieId": "gemeente-amsterdam",
  "bioVersie": "2025.1",
  "totaalMaatregelen": 162,
  "score": 0.0,
  "perCategorie": {
    "Organisatorische maatregelen": {"totaal": 72, "onbekend": 72},
    "Technologische maatregelen": {"totaal": 66, "onbekend": 66},
    ...
  }
}
```

Het rapport is aligned met ENSIA: per maatregel een status (compliant/niet-compliant/onbekend) en per categorie een score.

## ENSIA Alignment

ENSIA (Elektronische Normering Systeem Informatiebeveiliging Ambtenaren) is het systeem waarmee overheidsorganisaties BIO-compliance rapporteren. JuraRegel kan de rule engine achter ENSIA worden:

1. Organisatie voert in: "maatregel 5.01.01 is geïmplementeerd"
2. JuraRegel checkt: "is dit voldoende voor BIO2 maatregel 5.01.01?"
3. JuraRegel retourneert: "compliant ja/nee + ISO referentie + ontbrekende elementen"
4. Audit trail wordt opgeslagen voor ENSIA rapportage

## CIP Adoptie Pad

Het CIP (Centrum voor Informatiebeveiliging en Privacybescherming) beheert de BIO. Adoptie stappen:
1. CIP reviewt de 162 RegelSpraak regels (HUMAN-GATE)
2. CIP accordeert compliance rapport format (ENSIA aligned)
3. CIP promoot JuraRegel als compliance tool naar overheidsorganisaties
4. Overheidsorganisaties gebruiken Rule API voor self-assessment

## Validatie

| Metriek | Waarde |
|---|---|
| Maatregelen geparsed | 167 (van MinBZK GitHub) |
| Overheidsmaatregelen in JREM | 162 |
| ISO-only maatregelen | 5 |
| Tests | 18 (alle groen) |
| CI gates | 14 (9 PASS, 5 SKIP) |
| API endpoints | 7 |
| ISO bronverwijzingen | 162 (alle regels) |
