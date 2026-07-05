#!/bin/bash
set -uo pipefail
ROOT_DIR=$(cd $(dirname "$0")/.. && pwd)
cd "$ROOT_DIR"
echo "=== Legal Review Check ==="
python3 ci/legal-review-gate.py
echo "=== Legal Review Complete ==="
