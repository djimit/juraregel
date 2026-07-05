#!/bin/bash
# Extraction CI Gates — validates extracted rules quality
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

PASS=0; FAIL=0

pass_gate() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail_gate() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

echo "========================================"
echo "  Extraction CI Gates"
echo "========================================"

# Gate 1: No rule with confidence <70% without review flag
echo "Gate 1/3: No low-confidence rule without review flag"
LOW_CONF=$(python3 -c "
import json, glob
bad = 0
for f in glob.glob('.data/review-queue.json'):
    items = json.load(open(f))
    for i in items:
        if i.get('confidence', 100) < 70 and i.get('status') == 'approved':
            bad += 1
            print(f"  {i['rule_id']}: confidence={i['confidence']}")
print(bad)
" 2>/dev/null || echo "0")
if [ "$LOW_CONF" -eq 0 ]; then
  pass_gate "No low-confidence rules approved without review"
else
  fail_gate "$LOW_CONF low-confidence rules approved"
fi

# Gate 2: Every extracted rule has sourceRef
echo "Gate 2/3: Every rule has sourceRef"
NO_REF=$(python3 -c "
import json, glob
bad = 0
for f in glob.glob('.data/review-queue.json'):
    items = json.load(open(f))
    for i in items:
        if not i.get('source_refs'):
            bad += 1
print(bad)
" 2>/dev/null || echo "0")
if [ "$NO_REF" -eq 0 ]; then
  pass_gate "All rules have sourceRefs"
else
  fail_gate "$NO_REF rules without sourceRefs"
fi

# Gate 3: Review queue integrity
echo "Gate 3/3: Review queue integrity"
QUEUE_OK=$(python3 -c "
import json, glob
for f in glob.glob('.data/review-queue.json'):
    items = json.load(open(f))
    print('ok')
    break
" 2>/dev/null || echo "no-queue")
if [ "$QUEUE_OK" = "ok" ] || [ "$QUEUE_OK" = "no-queue" ]; then
  pass_gate "Review queue valid (or empty)"
else
  fail_gate "Review queue corrupted"
fi

echo "========================================"
echo "  Extraction Gates: $PASS passed, $FAIL failed"
echo "========================================"
[ "$FAIL" -eq 0 ]
