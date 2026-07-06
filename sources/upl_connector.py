"""
UPL Connector.

Bron: standaarden.overheid.nl/owms/oquery/UPL-actueel.json
"""
import json
import urllib.request

from sources.base import BaseConnector

UPL_URL = "https://standaarden.overheid.nl/owms/oquery/UPL-actueel.json"
UPL_PAGE = "https://standaarden.overheid.nl/upl"


def _value(binding: dict, key: str, default: str = "") -> str:
    return binding.get(key, {}).get("value", default)


def _marked(binding: dict, key: str) -> bool:
    return _value(binding, key).strip().lower() in {"x", "j", "ja", "true", "1"}


class UPLConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        try:
            req = urllib.request.Request(UPL_URL, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return self.normalize(resp.read().decode())["products"]
        except Exception as e:
            return [{"error": str(e), "source": "UPL"}]

    def get_document(self, doc_id: str) -> dict:
        needle = doc_id.casefold()
        for product in self.list_sources():
            if product.get("name", "").casefold() == needle or product.get("id", "").casefold() == needle:
                return product
        return {"error": "not_found", "id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        # ponytail: UPL has release cadence, not per-item update metadata in this endpoint.
        return self.list_sources() if not last_check else []

    def normalize(self, raw_data: str) -> dict:
        data = json.loads(raw_data)
        products = []
        for binding in data.get("results", {}).get("bindings", []):
            name = _value(binding, "UniformeProductnaam").strip()
            uri = _value(binding, "URI").strip()
            if not name:
                continue
            bestuurslagen = [
                layer.casefold()
                for layer in ("Rijk", "Provincie", "Waterschap", "Gemeente")
                if _marked(binding, layer)
            ]
            products.append({
                "id": uri.rsplit("/", 1)[-1] if uri else name.replace(" ", "-"),
                "name": name,
                "uri": uri,
                "bestuurslagen": bestuurslagen,
                "doelgroepen": [
                    target.casefold()
                    for target in ("Burger", "Bedrijf")
                    if _marked(binding, target)
                ],
                "signals": {
                    "sdg": bool(_value(binding, "SDG").strip()),
                    "aanvraag": _marked(binding, "Aanvraag"),
                    "melding": _marked(binding, "Melding"),
                    "verplichting": _marked(binding, "Verplichting"),
                    "subsidie": _marked(binding, "Subsidie"),
                    "wmebv": _marked(binding, "Wmebv"),
                },
                "sourceRefs": [{
                    "type": "regeling",
                    "title": "Uniforme Productnamenlijst (UPL)",
                    "section": name,
                    "url": UPL_PAGE,
                }],
                "legalBasis": {
                    "label": _value(binding, "Grondslaglabel"),
                    "url": _value(binding, "Grondslaglink"),
                },
            })
        return {"source": "UPL", "products": products, "count": len(products)}

    def health_check(self) -> dict:
        try:
            req = urllib.request.Request(UPL_URL, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "UPL", "status": "ok", "http_code": resp.status}
        except Exception as e:
            return {"source": "UPL", "status": "error", "error": str(e)}


if __name__ == "__main__":
    print(json.dumps(UPLConnector().health_check(), indent=2))
