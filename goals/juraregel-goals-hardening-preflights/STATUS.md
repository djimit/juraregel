# JuraRegel Goals Hardening And Preflights Status

## Current State

Implemented on 2026-07-06 from `/Users/dlandman/juraregel`.

## Evidence Lock

- Host: MacBook-Pro
- OS: Darwin
- Target repo: `/Users/dlandman/juraregel`
- OpenSpec change: `/Users/dlandman/openspec/changes/juraregel-goals-hardening-preflights`

## Progress

- [x] Goal created
- [x] Baseline captured
- [x] Jurist-acceptatie readiness
- [x] Source health cleanup
- [x] BWB traceability cleanup
- [x] Decentrale regelcheck
- [x] Woo publicatieplicht preflight
- [x] STTR/RTR preflight
- [x] Validation

## Validation

- `.venv/bin/python -m pytest` -> 505 passed, 15 warnings.
- `.venv/bin/python tools/jkb-builder.py` -> 690 rules indexed, 30 domains, PASS.
- `.venv/bin/python tools/jkb-builder.py --check-only` -> valid true, JREM count 690, index count 690.
- All JREM exports against `shared/jrem-schema.json` -> 33 exports valid.
- `.venv/bin/python ci/validate-jrem.py` -> 0 errors, 0 warnings.
- `.venv/bin/python sources/scheduler.py --health` -> BWB, EUR-Lex, Rechtspraak, UPL, TOOI/ROO, CVDR/SRU, Woo-index/DiWoo, STTR/IMTR+RTR ok; PLOOI deprecated and reachable.
- `openspec validate juraregel-goals-hardening-preflights --strict` -> valid.
- `git diff --check` -> clean.

## Residual Risk

- All new use cases are L1 PoC and `acceptatieType=draft`; production status still requires final jurist-acceptatie metadata.
- PLOOI is classified as deprecated rather than an authoritative active API source.
- New connectors use fixture-first normalizers; live harvesters remain out of scope for this change.
