#!/bin/bash
# Legal Review Gate - waarschuwt bij self-approved regels
set -euo pipefail
ROOT_DIR=$(cd $(dirname $0)/.. && pwd)
cd $ROOT_DIR

echo "=== Legal Review Check ==="

WARN=0
for f in use-cases/*/jrem/exports/*.json; do
  [ -f "$f" ] || continue
  TYPE=$(python3 -c "import json; d=json.load(open("$f")); print(d.get("approval",{}).get("type","none"))" 2>/dev/null || echo "none")
  if [ "$TYPE" = "self" ]; then
    echo "  WARN: $f is self-approved (not legally validated)"
    WARN=$((WARN + 1))
  fi
done

echo "Checked all JREM exports: $WARN self-approved"

if [ "$WARN" -gt 0 ]; then
  echo "WARNING: $WARN exports are self-approved. Legal review recommended."
  # Non-blocking: exit 0 but warn
  # Change to exit 1 to block CI
fi

echo "=== Legal Review Complete ==="
