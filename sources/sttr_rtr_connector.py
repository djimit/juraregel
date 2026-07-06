"""
STTR/IMTR + RTR connector for applicable-rule package preflights.

Bron: Informatiepunt Leefomgeving
"""
import json
import urllib.request

from sources.base import BaseConnector

STTR_PAGE = "https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


class STTRRTRConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def normalize(self, raw_data: str) -> dict:
        data = json.loads(raw_data)
        packages = []
        for package in data.get("packages", []):
            packages.append({
                "packageId": _norm(package.get("packageId")),
                "packageLabel": package.get("packageId", ""),
                "sttrVersion": package.get("sttrVersion", ""),
                "imtrVersion": package.get("imtrVersion", ""),
                "rtrVersion": package.get("rtrVersion", ""),
                "status": package.get("status", ""),
                "issues": package.get("issues", []),
                "jremMapping": package.get("jremMapping", {}),
                "sourceRefs": package.get("sourceRefs", []),
            })
        return {"source": "STTR/IMTR+RTR", "packages": packages, "count": len(packages)}

    def health_check(self) -> dict:
        try:
            req = urllib.request.Request(
                STTR_PAGE,
                headers={"User-Agent": "JuraRegel source-health/2026.1"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "STTR/IMTR+RTR", "status": "ok", "http_code": resp.status, "checked_url": STTR_PAGE}
        except Exception as e:
            return {"source": "STTR/IMTR+RTR", "status": "error", "error": str(e)}
