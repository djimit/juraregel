"""Griffierecht Rule API — use case app die shared/api_base.py factory gebruikt."""
import sys
from pathlib import Path

SHARED_DIR = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED_DIR))
from api_base import create_app

JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("griffierecht", JREM_DIR, 8490)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8490)
