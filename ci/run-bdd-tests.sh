#!/bin/bash
set -euo pipefail
ROOT_DIR=$(cd $(dirname $0)/.. && pwd)
cd $ROOT_DIR
echo BDD Tests
PYTHON=${PYTHON:-python3}
$PYTHON -m pytest features/ -v --tb=short 2>&1
echo Complete
