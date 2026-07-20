#!/bin/bash
# Honest scoped check for one use case. Repository-wide policy gates remain
# global because maturity and source-quality rules are shared contracts.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

UC_DIR="${1:-use-cases/griffierecht}"
case "$UC_DIR" in
  use-cases/*) ;;
  *) echo "Use-case path must be below use-cases/" >&2; exit 2 ;;
esac
if [ ! -d "$UC_DIR" ]; then
  echo "Unknown use case: $UC_DIR" >&2
  exit 2
fi

PYTHON="$ROOT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON=python3
fi

echo "JuraRegel scoped gates: $UC_DIR"
"$PYTHON" ci/check-schema.py

found_export=0
for export in "$UC_DIR"/jrem/exports/*.json; do
  [ -f "$export" ] || continue
  found_export=1
  "$PYTHON" shared/validate.py \
    --schema shared/jrem-schema-v1.1.0.json \
    --instance "$export"
done
if [ "$found_export" -eq 0 ]; then
  echo "No JREM exports found in $UC_DIR" >&2
  exit 1
fi

"$PYTHON" ci/validate-rule-semantics.py
"$PYTHON" ci/source_quality.py

if find "$UC_DIR/tests" -type f -name 'test_*.py' -print -quit 2>/dev/null | grep -q .; then
  "$PYTHON" -m pytest "$UC_DIR/tests" -q --no-header
else
  echo "No domain-specific tests; validating the catalog capability contract"
  "$PYTHON" -m pytest ci/test_catalog_contracts.py -q --no-header
fi

bash ci/legal-review-gate.sh
echo "Scoped executable gates passed: $UC_DIR"
