"""
TOOI/ROO Connector.

Bron: standaarden.overheid.nl/tooi/waardelijsten/
"""
import json
import urllib.request

from sources.base import BaseConnector

TOOI_PAGE = "https://standaarden.overheid.nl/tooi/waardelijsten/"
TOOI_SOURCES = {
    "gemeente": "https://repository.officiele-overheidspublicaties.nl/waardelijsten/rwc_gemeenten_compleet/5/json/rwc_gemeenten_compleet_5.json",
    "provincie": "https://repository.officiele-overheidspublicaties.nl/waardelijsten/rwc_provincies_compleet/1/json/rwc_provincies_compleet_1.json",
    "waterschap": "https://repository.officiele-overheidspublicaties.nl/waardelijsten/rwc_waterschappen_compleet/2/json/rwc_waterschappen_compleet_2.json",
    "rijk": "https://repository.officiele-overheidspublicaties.nl/waardelijsten/rwc_ministeries_compleet/6/json/rwc_ministeries_compleet_6.json",
}

RDF_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
ORG_CODE = "https://identifier.overheid.nl/tooi/def/ont/organisatiecode"
NAME_EXCL = "https://identifier.overheid.nl/tooi/def/ont/voorkeursnaamExclSoort"
NAME_INCL = "https://identifier.overheid.nl/tooi/def/ont/voorkeursnaamInclSoort"


def _first(data: dict, key: str) -> str:
    values = data.get(key, [])
    if not values:
        return ""
    first = values[0]
    return first.get("@value") or first.get("@id") or ""


def _layer(types: list[str]) -> str:
    joined = " ".join(types).casefold()
    if "gemeente" in joined:
        return "gemeente"
    if "provincie" in joined:
        return "provincie"
    if "waterschap" in joined:
        return "waterschap"
    if "ministerie" in joined:
        return "rijk"
    return "overheid"


class TOOIROOConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        records = []
        errors = []
        for layer, url in TOOI_SOURCES.items():
            try:
                req = urllib.request.Request(url, headers={"Accept": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    records.extend(self._normalize_items(resp.read().decode(), layer, url))
            except Exception as e:
                errors.append({"error": str(e), "source": "TOOI/ROO", "bestuurslaag": layer})
        return records or errors

    def get_document(self, doc_id: str) -> dict:
        needle = doc_id.casefold()
        for org in self.list_sources():
            values = (org.get("id", ""), org.get("code", ""), org.get("name", ""), org.get("officialName", ""))
            if any(v.casefold() == needle for v in values):
                return org
        return {"error": "not_found", "id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        # ponytail: TOOI waardelijsten are immutable per published URL; update discovery is a page check.
        return self.list_sources() if not last_check else []

    def normalize(self, raw_data: str) -> dict:
        records = self._normalize_items(raw_data, "overheid", TOOI_PAGE)
        return {"source": "TOOI/ROO", "organisations": records, "count": len(records)}

    def _normalize_items(self, raw_data: str, fallback_layer: str, source_url: str) -> list[dict]:
        data = json.loads(raw_data)
        records = []
        for item in data:
            types = item.get("@type", [])
            layer = _layer(types) if types else fallback_layer
            code = _first(item, ORG_CODE)
            name = _first(item, NAME_EXCL) or _first(item, RDF_LABEL)
            official = _first(item, NAME_INCL) or _first(item, RDF_LABEL)
            if not (code or name):
                continue
            records.append({
                "id": item.get("@id", code),
                "code": code,
                "name": name,
                "officialName": official,
                "bestuurslaag": layer,
                "organisationClass": types[-1].rsplit("/", 1)[-1] if types else fallback_layer,
                "sourceRefs": [{
                    "type": "regeling",
                    "title": "TOOI/ROO waardelijst",
                    "section": layer,
                    "url": source_url,
                }],
            })
        return records

    def health_check(self) -> dict:
        try:
            req = urllib.request.Request(TOOI_PAGE, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "TOOI/ROO", "status": "ok", "http_code": resp.status}
        except Exception as e:
            return {"source": "TOOI/ROO", "status": "error", "error": str(e)}


if __name__ == "__main__":
    print(json.dumps(TOOIROOConnector().health_check(), indent=2))
