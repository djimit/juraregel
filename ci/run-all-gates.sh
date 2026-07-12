#!/bin/bash
# Canonical repository gate. Every step executes a real contract; no synthetic
# per-domain pass counts or empty test-class gates.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON="$ROOT_DIR/.venv/bin/python"
if [ ! -x "$PYTHON" ]; then
  PYTHON=python3
fi

echo "JuraRegel repository gates"

"$PYTHON" -m compileall -q shared sources tools mcp-server use-cases ci features
"$PYTHON" ci/check-schema.py
"$PYTHON" ci/validate-rule-semantics.py
"$PYTHON" ci/source_quality.py
"$PYTHON" ci/validate-jrem.py
"$PYTHON" tools/generate_openapi.py
"$PYTHON" -m pytest \
  use-cases/*/tests/ ci/test_*.py mcp-server/test_*.py features/ \
  sources/test_*.py shared/test_*.py tools/test_*.py \
  tools/rule-extraction/test_*.py governance/test_*.py \
  -q --no-header
bash ci/jkb-gates.sh
bash ci/legal-review-gate.sh
"$PYTHON" ci/l2_promotion_preflight.py
node bin/juraregel.mjs --help >/dev/null
npm ci --prefix sdk/typescript --ignore-scripts
npm --prefix sdk/typescript run check

echo "All executable repository gates passed"
