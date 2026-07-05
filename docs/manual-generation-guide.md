# Manual JREM Generation Guide

De RegelSpraak → JREM vertaling is momenteel handmatig. ALEF/MPS als geautomatiseerde generator is gepland voor v2.0.

## Stappen

1. **Verzamel bronnen** — wet, regeling, standaard, PDF, Markdown
2. **Schrijf begrippen** in `regelspraak/begrippen.rspraak`
3. **Schrijf regels** in `regelspraak/regels-YYYY.rspraak` (CNL, leesbaar door jurist)
4. **Maak JREM export** — gebruik parser script (indien beschikbaar) of handmatig
5. **Maak Rule API** — `create_app("<domein>", <jrem_path>, <port>)`
6. **Schrijf tests** — TestHealth, TestCheck, TestJREMValidation, TestIdempotentie
7. **Run CI** — `bash ci/run-gates.sh use-cases/<domein>`

## Automated Generation (v1.1+)

```bash
npx juraregel generate bio2        # Run bio2_parser.py
npx juraregel generate ncsc         # Run ncsc_parser.py
```

## ALEF/MPS (v2.0 — niet gestart)

ALEF (Adaptive Law Expression Framework) op MPS (Meta Programming System) zal:
- RegelSpraak → JREM automatisch genereren
- Een IDE bieden voor juristen met syntax highlighting
- Versie diffs tonen tussen regelversies
- Scenario's automatisch genereren uit beslistabellen

Tot ALEF beschikbaar is, gebruiken we handmatige vertaling of parser scripts.
