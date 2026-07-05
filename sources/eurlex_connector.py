"""
EUR-Lex Connector.

Bron: eur-lex.europa.eu
API: SPARQL endpoint + REST API
"""
import json
import urllib.request
import urllib.parse
from sources.base import BaseConnector

EURLEX_SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
EURLEX_REST = "https://eur-lex.europa.eu"

class EURLexConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        """List recent EU legislation."""
        return self.search_eu_legislation("regulation", limit=10)

    def get_document(self, doc_id: str) -> dict:
        """Get specific EU document by CELEX ID."""
        try:
            url = f"{EURLEX_REST}/legal-content/EN/TXT/?uri=CELEX:{doc_id}"
            with urllib.request.urlopen(url, timeout=30) as resp:
                return {"celex_id": doc_id, "html": resp.read().decode()[:5000], "url": url}
        except Exception as e:
            return {"error": str(e), "celex_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        """Check for new EU legislation since last_check."""
        return self.search_eu_legislation("directive", limit=5)

    def normalize(self, raw_data: str) -> dict:
        """Normalize EU HTML/XML to structured dict."""
        return {"source": "eur-lex", "length": len(raw_data), "format": "html"}

    def search_eu_legislation(self, query: str = "AI Act", doc_type: str = "regulation", limit: int = 10) -> list[dict]:
        """Search EU legislation via SPARQL."""
        sparql = f"""
        PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
        SELECT ?celex ?title ?date WHERE {{
            ?act a cdm:act_legislation .
            ?act cdm:act_celex_id ?celex .
            ?act dcterms:title ?title .
            ?act cdm:act_date_document ?date .
            FILTER(CONTAINS(LCASE(?title), LCASE("{query}")))
        }} LIMIT {limit}
        """
        try:
            data = urllib.parse.urlencode({"query": sparql, "format": "json"}).encode()
            req = urllib.request.Request(EURLEX_SPARQL, data=data, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                bindings = result.get("results", {}).get("bindings", [])
                return [{"celex": b.get("celex", {}).get("value", ""), "title": b.get("title", {}).get("value", "")} for b in bindings]
        except Exception as e:
            return [{"error": str(e)}]

    def health_check(self) -> dict:
        """Check EUR-Lex SPARQL endpoint."""
        try:
            data = urllib.parse.urlencode({"query": "SELECT * WHERE {?s ?p ?o} LIMIT 1", "format": "json"}).encode()
            req = urllib.request.Request(EURLEX_SPARQL, data=data)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "EUR-Lex", "status": "ok", "http_code": resp.status}
        except Exception as e:
            return {"source": "EUR-Lex", "status": "error", "error": str(e)}

if __name__ == "__main__":
    c = EURLexConnector()
    print(json.dumps(c.health_check(), indent=2))
