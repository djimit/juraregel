import sys
from pathlib import Path
SHARED = Path(__file__).parent.parent.parent.parent / "shared"
sys.path.insert(0, str(SHARED))
from api_base import create_app
JREM_DIR = Path(__file__).parent.parent / "jrem" / "exports"
app = create_app("api-registratie", JREM_DIR, 8510)
if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="127.0.0.1", port=8510)
