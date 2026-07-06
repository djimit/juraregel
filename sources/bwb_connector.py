"""
BWB (Basisvoorziening Wetgeving) Connector.

Bron: wetten.overheid.nl
API: REST (XML)
"""
import json
import urllib.request
import urllib.error
from pathlib import Path
from sources.base import BaseConnector

BWB_BASE = "https://wetten.overheid.nl"

class BWBConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        """List available laws from BWB."""
        try:
            url = f"{BWB_BASE}/api/v1/wetten"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            return [{"error": str(e)}]

    def get_document(self, doc_id: str) -> dict:
        """Get a specific law by BWB-ID."""
        try:
            url = f"{BWB_BASE}/xml/{doc_id}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                return {"bwb_id": doc_id, "xml": resp.read().decode(), "url": url}
        except Exception as e:
            return {"error": str(e), "bwb_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        """Check for updated laws since last_check."""
        sources = self.list_sources()
        if sources and "error" in sources[0]:
            return sources
        return [s for s in sources if s.get("mutatieDatum", "") > (last_check or "")]

    def normalize(self, raw_data: str) -> dict:
        """Normalize BWB-XML to structured dict."""
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw_data)
        return {
            "titel": root.findtext(".//Titel", ""),
            "bwb_id": root.findtext(".//BWB_Id", ""),
            "artikelen": len(root.findall(".//Artikel")),
        }

    def health_check(self) -> dict:
        """Check BWB endpoint."""
        try:
            url = f"{BWB_BASE}/BWBR0033715"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "JuraRegel source-health/2026.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {
                    "source": "BWB",
                    "status": "ok",
                    "http_code": resp.status,
                    "checked_url": url,
                }
        except Exception as e:
            return {"source": "BWB", "status": "error", "error": str(e)}

if __name__ == "__main__":
    c = BWBConnector()
    print(json.dumps(c.health_check(), indent=2))
