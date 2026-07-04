#!/bin/bash
# CI Legal Validation — per use case. 14 gates.
# Usage: bash ci/run-gates.sh [use-case-dir]
set -euo pipefail

UC_DIR="${1:-use-cases/griffierecht}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SHARED="$ROOT_DIR/shared"

if [ -f "$ROOT_DIR/.venv/bin/activate" ]; then source "$ROOT_DIR/.venv/bin/activate"; fi

GATES_PASSED=0; GATES_FAILED=0; GATES_SKIPPED=0; UC_NAME=$(basename "$UC_DIR")

gate_pass() { echo "  ✅ PASS: $1"; GATES_PASSED=$((GATES_PASSED + 1)); }
gate_fail() { echo "  ❌ FAIL: $1"; GATES_FAILED=$((GATES_FAILED + 1)); }
gate_skip() { echo "  ⏭️  SKIP: $1"; GATES_SKIPPED=$((GATES_SKIPPED + 1)); }

echo "═══════════════════════════════════════════════════════════"
echo "  CI Gates — $UC_NAME"
echo "═══════════════════════════════════════════════════════════"

# Gate 1: RegelSpraak syntax
echo "Gate 1/14: RegelSpraak syntax"
RS_DIR="$UC_DIR/regelspraak"
if [ -d "$RS_DIR" ]; then
  RS_FILES=$(find "$RS_DIR" -name "*.rspraak" 2>/dev/null | wc -l | tr -d " ")
  if [ "$RS_FILES" -gt 0 ]; then
    ERRORS=0
    for f in $(find "$RS_DIR" -name "*.rspraak" ! -name "begrippen.rspraak" 2>/dev/null); do
      grep -q "^regel " "$f" || ERRORS=$((ERRORS+1))
    done
    [ "$ERRORS" -eq 0 ] && gate_pass "$RS_FILES files, alle regel-bestanden bevatten regels" || gate_fail "$ERRORS file(s) zonder regels"
  else gate_skip "Geen .rspraak bestanden"; fi
else gate_skip "Geen regelspraak dir"; fi
echo "Gate 2/14: JREM schema"
[ -f "$SHARED/jrem-schema.json" ] && python3 -c "import json,jsonschema; jsonschema.Draft202012Validator.check_schema(json.load(open('$SHARED/jrem-schema.json')))" 2>/dev/null && gate_pass "Schema valid 2020-12" || gate_fail "Schema invalid"

# Gate 3: JREM export validatie
echo "Gate 3/14: JREM export validatie"
EXPORT_ERR=0; for f in "$UC_DIR"/jrem/exports/*.json; do [ -f "$f" ] && python3 "$SHARED/validate.py" --schema "$SHARED/jrem-schema.json" --instance "$f" >/dev/null 2>&1 || EXPORT_ERR=$((EXPORT_ERR+1)); done
[ "$EXPORT_ERR" -eq 0 ] && gate_pass "Alle exports valideren" || gate_fail "$EXPORT_ERR export(s) invalid"

# Gate 4: Brontraceability
echo "Gate 4/14: Brontraceability"
TRACE_ERR=0; for f in "$UC_DIR"/jrem/exports/*.json; do [ -f "$f" ] && python3 -c "import json; d=json.load(open('$f')); [print(r['ruleId']) for r in d.get('rules',[]) if not r.get('sourceRefs')]" 2>/dev/null | head -1 | grep -q . && TRACE_ERR=$((TRACE_ERR+1)) || true; done
[ "$TRACE_ERR" -eq 0 ] && gate_pass "Alle regels hebben sourceRefs" || gate_fail "$TRACE_ERR regel(s) zonder sourceRefs"

# Gate 5: Geldigheidsvalidatie
echo "Gate 5/14: Geldigheidsvalidatie"
VAL_ERR=0; for f in "$UC_DIR"/jrem/exports/*.json; do [ -f "$f" ] && python3 -c "import json; d=json.load(open('$f')); assert 'validFrom' in d and 'validUntil' in d" 2>/dev/null || VAL_ERR=$((VAL_ERR+1)); done
[ "$VAL_ERR" -eq 0 ] && gate_pass "validFrom/validUntil aanwezig" || gate_fail "$VAL_ERR export(s) zonder geldigheid"

# Gates 6-12: Tests
TESTS_DIR="$UC_DIR/tests"
if [ -d "$TESTS_DIR" ]; then
  for gate_class in "TestHappyPath:6:Unit tests" "TestNegativeCases:7:Negative" "TestBoundaryCases:8:Boundary" "TestRegression:9:Regression" "TestExplainability:10:Explainability" "TestAudit:11:Audit" "TestIdempotentie:12:Idempotentie"; do
    IFS=':' read -r cls num name <<< "$gate_class"
    echo "Gate $num/14: $name"
    COUNT=$(python3 -m pytest "$TESTS_DIR/" -k "$cls" --co -q 2>/dev/null | grep -c "::" || true)
    if [ "$COUNT" -gt 0 ]; then
      python3 -m pytest "$TESTS_DIR/" -k "$cls" -q --no-header 2>/dev/null && gate_pass "$name ($COUNT tests)" || gate_fail "$name faalden"
    else
      gate_skip "$name — geen tests voor deze klasse"
    fi
  done
  echo "Gate 13/14: JREM schema + scenarios"
  COUNT=$(python3 -m pytest "$TESTS_DIR/" -k "TestJREMValidation or TestJREMScenarios" --co -q 2>/dev/null | grep -c "::" || true)
  if [ "$COUNT" -gt 0 ]; then
    python3 -m pytest "$TESTS_DIR/" -k "TestJREMValidation or TestJREMScenarios" -q --no-header 2>/dev/null && gate_pass "Schema + scenarios ($COUNT tests)" || gate_fail "Schema/scenarios faalden"
  else
    gate_skip "Schema + scenarios — geen tests"
  fi
else
  for i in 6 7 8 9 10 11 12 13; do echo "Gate $i/14: Tests"; gate_skip "Geen tests dir"; done
fi

# Gate 14: Jurist-acceptatie
echo "Gate 14/14: Jurist-acceptatie"
ACC_ERR=0; for f in "$UC_DIR"/jrem/exports/*.json; do [ -f "$f" ] && python3 "$ROOT_DIR/ci/acceptatie-check.py" "$f" 2>&1 | grep -q "FAIL" && ACC_ERR=$((ACC_ERR+1)) || true; done
[ "$ACC_ERR" -eq 0 ] && gate_pass "Acceptatie check (SKIP voor drafts)" || gate_fail "$ACC_ERR acceptatie failure(s)"

echo "═══════════════════════════════════════════════════════════"
echo "  $UC_NAME: $GATES_PASSED passed, $GATES_FAILED failed, $GATES_SKIPPED skipped"
echo "═══════════════════════════════════════════════════════════"
[ "$GATES_FAILED" -eq 0 ]
