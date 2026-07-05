#!/bin/bash
# CI Driver — runt gates per use case + totaal overzicht.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TOTAL_PASS=0; TOTAL_FAIL=0; TOTAL_SKIP=0

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Legal RuleOps Platform — CI All Gates                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"

for uc in use-cases/*/; do
  [ -d "$uc" ] || continue
  bash ci/run-gates.sh "$uc" 2>&1 
done

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  Alle use cases: see per-use-case results above           ║"

echo ""
echo "=== JKB Gates ==="
bash ci/jkb-gates.sh 2>&1 

echo ""
echo "=== Alle gates voltooid ==="
echo "╚═══════════════════════════════════════════════════════════╝"
