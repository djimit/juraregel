#!/bin/bash
set -uo pipefail
ROOT_DIR=$(cd $(dirname "$0")/.. && pwd)
cd "$ROOT_DIR"
echo "=== Legal Review Check ==="
CI_MODE=${JURAREGEL_CI_MODE:-poc}
python3 ci/legal-review-gate.py
RC=$?
if [ $RC -ne 0 ]; then
  if [ "$CI_MODE" = "poc" ]; then
    echo "LEGAL_REVIEW_WARNING: self-approved exports (allowed in PoC mode)"
    exit 0
  else
    echo "LEGAL_REVIEW_FAIL: self-approved exports not allowed in $CI_MODE mode"
    exit 1
  fi
fi
echo "=== Legal Review Complete ==="
