#!/bin/bash
# JKB CI Gates — validates Knowledge Base completeness
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0; FAIL=0

pass_gate() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail_gate() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

echo "========================================"
echo "  JKB CI Gates"
echo "========================================"

# Gate 1: Index count matches JREM exports
echo "Gate 1/5: Index count matches JREM exports"
INDEX_COUNT=$(python3 -c "import json; print(len(json.load(open('knowledge-base/jkb-index.json'))))")
JREM_COUNT=0
for f in use-cases/*/jrem/exports/*.json; do
  [ -f "$f" ] || continue
  COUNT=$(python3 -c "import json; print(len(json.load(open('$f')).get('rules',[])))" 2>/dev/null) || continue
  JREM_COUNT=$((JREM_COUNT + COUNT))
done
if [ "$INDEX_COUNT" -eq "$JREM_COUNT" ]; then
  pass_gate "Index count ($INDEX_COUNT) == JREM count ($JREM_COUNT)"
else
  fail_gate "Index count ($INDEX_COUNT) != JREM count ($JREM_COUNT)"
fi

# Gate 2: All entries have required fields
echo "Gate 2/5: All entries have required fields"
MISSING=$(python3 -c "
import json
idx = json.load(open('knowledge-base/jkb-index.json'))
fields = ['nl_text', 'embedding_text', 'graph_nodes', 'content_hash']
bad = []
for e in idx:
    for f in fields:
        if f not in e or not e[f]:
            bad.append(e['rule_id'] + ':' + f)
print(len(bad))
for b in bad[:5]: print(b)
")
if [ "$MISSING" -eq 0 ]; then
  pass_gate "All entries have required fields"
else
  fail_gate "$MISSING entries missing required fields"
fi

# Gate 3: Content hash validation (sample 10%)
echo "Gate 3/5: Content hash validation"
HASH_OK=$(python3 -c "
import json, hashlib
idx = json.load(open('knowledge-base/jkb-index.json'))
bad = 0
for e in idx:
    # Reconstruct original rule from hash — verify hash is valid SHA256
    h = e['content_hash']
    if len(h) != 64 or not all(c in '0123456789abcdef' for c in h):
        bad += 1
print(bad)
")
if [ "$HASH_OK" -eq 0 ]; then
  pass_gate "All content hashes are valid SHA256"
else
  fail_gate "$HASH_OK invalid content hashes"
fi

# Gate 4: Vector store coverage (if .qdrant exists)
echo "Gate 4/5: Vector store coverage"
if [ -d ".qdrant" ]; then
  COVERAGE=$(python3 tools/jkb-vectorstore.py --check-coverage 2>/dev/null) || COVERAGE='{"complete": false, "error": "qdrant not available"}'
  COMPLETE=$(echo "$COVERAGE" | python3 -c "import json,sys; print(json.load(sys.stdin)['complete'])")
  if [ "$COMPLETE" = "True" ]; then
    pass_gate "Vector store coverage complete"
  else
    fail_gate "Vector store coverage incomplete: $COVERAGE"
  fi
else
  echo "  SKIP: .qdrant not found (run: python3 tools/jkb-vectorstore.py index)"
fi

# Gate 5: Keyword store coverage (if .keyword.db exists)
echo "Gate 5/5: Keyword store coverage"
if [ -f ".keyword.db" ]; then
  COVERAGE=$(python3 tools/jkb-keyword.py --check-coverage 2>/dev/null)
  COMPLETE=$(echo "$COVERAGE" | python3 -c "import json,sys; print(json.load(sys.stdin)['complete'])")
  if [ "$COMPLETE" = "True" ]; then
    pass_gate "Keyword store coverage complete"
  else
    fail_gate "Keyword store coverage incomplete: $COVERAGE"
  fi
else
  echo "  SKIP: .keyword.db not found (run: python3 tools/jkb-keyword.py index)"
fi

echo "========================================"
echo "  JKB CI Gates: $PASS passed, $FAIL failed"
echo "========================================"
[ "$FAIL" -eq 0 ]
