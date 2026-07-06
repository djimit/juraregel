"""
CVDR/SRU connector for local regulation preflights.

Bron: lokaleregelgeving.overheid.nl
"""
import json
import urllib.request

from sources.base import BaseConnector

CVDR_PAGE = "https://lokaleregelgeving.overheid.nl/"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


def _postcode(value: str) -> str:
    return _norm(value).replace(" ", "")


class CVDRSRUConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def normalize(self, raw_data: str) -> dict:
        data = json.loads(raw_data)
        records = []
        for item in data.get("records", []):
            records.append({
                "postcode": _postcode(item.get("postcode")),
                "product": _norm(item.get("product")),
                "activiteit": _norm(item.get("activiteit")),
                "bestuurslaag": _norm(item.get("bestuurslaag")),
                "bevoegdGezag": item.get("bevoegdGezag", ""),
                "regeling": item.get("regeling", ""),
                "procedureType": item.get("procedureType", ""),
                "openNormen": item.get("openNormen", []),
                "sourceRefs": item.get("sourceRefs", []),
            })
        return {"source": "CVDR/SRU", "records": records, "count": len(records)}

    def health_check(self) -> dict:
        try:
            req = urllib.request.Request(
                CVDR_PAGE,
                headers={"User-Agent": "JuraRegel source-health/2026.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "CVDR/SRU", "status": "ok", "http_code": resp.status, "checked_url": CVDR_PAGE}
        except Exception as e:
            return {"source": "CVDR/SRU", "status": "error", "error": str(e)}
