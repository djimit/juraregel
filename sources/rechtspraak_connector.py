"""
Rechtspraak Open Data Connector.

Bron: data.rechtspraak.nl
API: Atom feed (XML)
"""
import json
import urllib.request
from sources.base import BaseConnector

RECHTSPRAAK_API = "https://data.rechtspraak.nl/uitspraken/zoeken"

class RechtspraakConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        """List recent court decisions."""
        return self.search_uitspraken(limit=10)

    def get_document(self, doc_id: str) -> dict:
        """Get specific decision by ECLI."""
        try:
            url = f"{RECHTSPRAAK_API}?ecli={doc_id}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                return {"ecli": doc_id, "xml": resp.read().decode()[:5000], "url": url}
        except Exception as e:
            return {"error": str(e), "ecli": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        """Check for new decisions since last_check."""
        return self.search_uitspraken(limit=5)

    def normalize(self, raw_data: str) -> dict:
        """Normalize Rechtspraak Atom feed."""
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw_data)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        return {"source": "rechtspraak", "count": len(entries)}

    def search_uitspraken(self, rechtsgebied: str = None, limit: int = 10) -> list[dict]:
        """Search court decisions."""
        try:
            params = {"max": limit}
            if rechtsgebied:
                params["subject"] = rechtsgebied
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{RECHTSPRAAK_API}?{query}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                data = resp.read().decode()
                import xml.etree.ElementTree as ET
                root = ET.fromstring(data)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                entries = root.findall("atom:entry", ns)
                return [{"ecli": e.find("atom:id", ns).text.split("/")[-1] if e.find("atom:id", ns) is not None else "", "title": e.find("atom:title", ns).text if e.find("atom:title", ns) is not None else ""} for e in entries]
        except Exception as e:
            return [{"error": str(e)}]

    def health_check(self) -> dict:
        """Check Rechtspraak endpoint."""
        try:
            url = f"{RECHTSPRAAK_API}?max=1"
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "Rechtspraak", "status": "ok", "http_code": resp.status}
        except Exception as e:
            return {"source": "Rechtspraak", "status": "error", "error": str(e)}

if __name__ == "__main__":
    c = RechtspraakConnector()
    print(json.dumps(c.health_check(), indent=2))
