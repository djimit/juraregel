#!/bin/bash
# JREM Schema Version Check - CI gate
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"
echo "=== JREM Schema Version Check ==="
python3 tools/jrem-migrate.py --check-only
