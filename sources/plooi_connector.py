"""
PLOOI (Platform Open Officiele Publicaties) Connector.

Bron: zoek.officielebekendmakingen.nl
"""
import json
import urllib.request
from sources.base import BaseConnector

PLOOI_API = "https://zoek.officielebekendmakingen.nl/api/v1"
PLOOI_PUBLIC = "https://zoek.officielebekendmakingen.nl"

class PLOOIConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        """List recent official publications."""
        try:
            url = f"{PLOOI_API}/publicaties?max=10"
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return [{"error": str(e)}]

    def get_document(self, doc_id: str) -> dict:
        """Get specific publication by ID."""
        try:
            url = f"{PLOOI_API}/publicatie/{doc_id}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return {"error": str(e), "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        """Check for new publications since last_check."""
        return self.list_sources()[:5]

    def normalize(self, raw_data: str) -> dict:
        """Normalize PLOOI data."""
        return {"source": "plooi", "length": len(raw_data)}

    def health_check(self) -> dict:
        """Check PLOOI endpoint."""
        try:
            url = PLOOI_PUBLIC
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "JuraRegel source-health/2026.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {
                    "source": "PLOOI",
                    "status": "deprecated",
                    "http_code": resp.status,
                    "checked_url": url,
                    "note": "Legacy PLOOI API is not used as an authoritative source; public publications portal is reachable.",
                }
        except Exception as e:
            return {"source": "PLOOI", "status": "error", "error": str(e)}

if __name__ == "__main__":
    c = PLOOIConnector()
    print(json.dumps(c.health_check(), indent=2))
