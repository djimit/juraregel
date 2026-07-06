"""
Source-expansion preflight spikes.

These are candidate source contracts, not production ingesters.
"""
import json
import urllib.request

SOURCE_SPIKES = [
    {
        "id": "cvdr-sru",
        "name": "Lokale wet- en regelgeving / CVDR + SRU",
        "useCase": "decentrale-regelcheck",
        "urls": [
            "https://lokaleregelgeving.overheid.nl/",
            "https://standaarden.overheid.nl/sru",
        ],
        "manualReviewBoundary": "Open lokale normen en beleidsruimte blijven handmatige review.",
    },
    {
        "id": "woo-diwoo",
        "name": "Woo-index + DiWoo/Woo-harvester",
        "useCase": "woo-publicatieplicht-preflight",
        "urls": [
            "https://organisaties.overheid.nl/woo",
            "https://standaarden.overheid.nl/diwoo/metadata",
        ],
        "manualReviewBoundary": "Preflight rapporteert metadata-gaps, publiceert geen documenten.",
    },
    {
        "id": "digitale-dienst-registers",
        "name": "DigiToegankelijk + API-register + data.overheid.nl",
        "useCase": "digitale-dienst-compliance-check",
        "urls": [
            "https://dashboard.digitoegankelijk.nl/",
            "https://apis.developer.overheid.nl/apis",
            "https://data.overheid.nl/data/api/3/",
        ],
        "manualReviewBoundary": "Statusdata wordt gelezen; geen organisatierapport publiceren zonder akkoord.",
    },
    {
        "id": "sttr-rtr",
        "name": "STTR/IMTR + RTR",
        "useCase": "sttr-preflight",
        "urls": [
            "https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/",
            "https://iplo.nl/digitaal-stelsel/aansluiten/toepasbare-regels-aanleveren/",
        ],
        "manualReviewBoundary": "Valideert leveringsfit; neemt geen omgevingsrechtelijke beslissing.",
    },
    {
        "id": "interoperable-europe-2024-903",
        "name": "EU Interoperable Europe Act 2024/903",
        "useCase": "interoperability-assessment-builder",
        "urls": [
            "https://eur-lex.europa.eu/eli/reg/2024/903/oj/eng",
        ],
        "manualReviewBoundary": "Machineleesbaar assessment publiceren pas na human approval.",
    },
]


def list_preflight_sources() -> list[dict]:
    return SOURCE_SPIKES


def get_preflight_source(source_id: str) -> dict:
    for source in SOURCE_SPIKES:
        if source["id"] == source_id:
            return source
    return {"error": "not_found", "id": source_id}


def health_check_source(source: dict) -> dict:
    results = []
    for url in source["urls"]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "JuraRegel source-spike"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                results.append({"url": url, "status": "ok", "http_code": resp.status})
        except Exception as e:
            results.append({"url": url, "status": "error", "error": str(e)})
    return {"source": source["id"], "checks": results}


if __name__ == "__main__":
    print(json.dumps(list_preflight_sources(), indent=2))
