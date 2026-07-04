#!/bin/bash
# JuraRegel use case scaffolder
# Usage: bash juraregel-init.sh <domein> <port>
set -euo pipefail

DOMAIN="${1:?Usage: juraregel-init.sh <domein> <port>}"
PORT="${2:?Usage: juraregel-init.sh <domein> <port>}"
DIR="use-cases/$DOMAIN"

mkdir -p "$DIR"/{regelspraak,jrem/exports,api,tests,lib}

cat > "$DIR/regelspraak/begrippen.rspraak" << EOF
// Begrippenmodel — $DOMAIN
begrip maatregelId: "Unieke identificatie." type: tekst.
begrip compliant: "Voldoet?" waarden: ja, nee, onbekend.
EOF

cat > "$DIR/api/app.py" << EOF
import sys
from pathlib import Path
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("$DOMAIN", JREM_DIR, $PORT)
if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=$PORT)
EOF

cat > "$DIR/tests/test_${DOMAIN}.py" << EOF
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("$DOMAIN", JREM_DIR, $PORT)
client = TestClient(app)

class TestHealth:
    def test_health(self): assert client.get("/v1/health").status_code == 200
    def test_domain(self): assert client.get("/v1/health").json()["domain"] == "$DOMAIN"
EOF

echo "✅ Use case '$DOMAIN' scaffolded at $DIR (port $PORT)"
echo "   Next: schrijf regels, maak JREM export, run tests"
