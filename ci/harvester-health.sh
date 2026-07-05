#!/bin/bash
set -euo pipefail
ROOT_DIR=$(cd $(dirname $0)/.. && pwd)
cd $ROOT_DIR
echo Harvester Health
python3 sources/harvester.py --health 2>&1 || echo SKIP
echo Complete
