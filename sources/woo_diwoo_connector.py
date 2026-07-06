"""
Woo-index/DiWoo connector for publication metadata preflights.

Bron: organisaties.overheid.nl/woo
"""
import json
import urllib.request

from sources.base import BaseConnector

WOO_INDEX_PAGE = "https://organisaties.overheid.nl/woo"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


class WooDiWooConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def normalize(self, raw_data: str) -> dict:
        data = json.loads(raw_data)
        documents = []
        for org in data.get("organisations", []):
            for doc in org.get("documents", []):
                documents.append({
                    "organisatie": _norm(org.get("organisatie")),
                    "organisatieLabel": org.get("organisatie", ""),
                    "tooiCode": org.get("tooiCode", ""),
                    "documentType": _norm(doc.get("documentType")),
                    "documentTypeLabel": doc.get("documentType", ""),
                    "location": doc.get("location", ""),
                    "metadata": doc.get("metadata", {}),
                    "sourceRefs": org.get("sourceRefs", []) + doc.get("sourceRefs", []),
                })
        return {"source": "Woo-index/DiWoo", "documents": documents, "count": len(documents)}

    def health_check(self) -> dict:
        try:
            req = urllib.request.Request(
                WOO_INDEX_PAGE,
                headers={"User-Agent": "JuraRegel source-health/2026.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "Woo-index/DiWoo", "status": "ok", "http_code": resp.status, "checked_url": WOO_INDEX_PAGE}
        except Exception as e:
            return {"source": "Woo-index/DiWoo", "status": "error", "error": str(e)}
