"""CVDR/SRU connector for local regulation preflights."""
import html
from html.parser import HTMLParser
import json
import re
from urllib.parse import urlencode, urljoin
import urllib.request

from sources.base import BaseConnector

CVDR_PAGE = "https://lokaleregelgeving.overheid.nl/"
CVDR_SEARCH = "https://lokaleregelgeving.overheid.nl/ZoekResultaat"
USER_AGENT = "JuraRegel source-health/2026.1"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


def _postcode(value: str) -> str:
    return _norm(value).replace(" ", "")


def _postcode_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")[:4]


class _ResultLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._capture = False
        self._href = ""
        self._text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        classes = attr.get("class", "")
        if tag == "h2" and "result--title" in classes:
            self._capture = True
        elif self._capture and tag == "a":
            self._href = attr.get("href", "")
            self._text = []

    def handle_data(self, data):
        if self._capture and self._href:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._capture and self._href:
            text = html.unescape(" ".join("".join(self._text).split()))
            if text:
                self.links.append({"title": text, "href": self._href})
            self._href = ""
            self._text = []
        elif tag == "h2" and self._capture:
            self._capture = False


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")


class CVDRSRUConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def live_search(
        self,
        postcode: str = "",
        product: str = "",
        activiteit: str = "",
        bestuursorgaan: str = "",
        bestuurslaag: str = "",
        limit: int = 10,
    ) -> dict:
        query_text = product or activiteit or bestuursorgaan
        params = {"count": str(limit)}
        postcode_digits = _postcode_digits(postcode)
        if postcode_digits:
            params["locatie"] = postcode_digits
        if query_text:
            params["tekst"] = query_text
        url = f"{CVDR_SEARCH}?{urlencode(params)}"
        try:
            raw = _fetch(url)
        except Exception as exc:
            return {
                "source": "CVDR/SRU",
                "status": "degraded",
                "error": str(exc),
                "checked_url": url,
                "records": [],
                "count": 0,
            }
        return self.parse_live_results(
            raw,
            checked_url=url,
            postcode=postcode,
            product=product,
            activiteit=activiteit,
            bestuursorgaan=bestuursorgaan,
            bestuurslaag=bestuurslaag,
            limit=limit,
        )

    def parse_live_results(
        self,
        raw_html: str,
        checked_url: str = CVDR_SEARCH,
        postcode: str = "",
        product: str = "",
        activiteit: str = "",
        bestuursorgaan: str = "",
        bestuurslaag: str = "",
        limit: int = 10,
    ) -> dict:
        parser = _ResultLinkParser()
        parser.feed(raw_html or "")
        records = []
        for link in parser.links[:limit]:
            detail_url = urljoin(CVDR_PAGE, link["href"])
            records.append({
                "postcode": _postcode(postcode),
                "product": _norm(product or activiteit),
                "activiteit": _norm(activiteit),
                "bestuurslaag": _norm(bestuurslaag),
                "bevoegdGezag": bestuursorgaan,
                "regeling": link["title"],
                "procedureType": "onbekend",
                "openNormen": ["Live CVDR-resultaat vereist inhoudelijke duiding"],
                "sourceRefs": [{
                    "type": "regeling",
                    "title": "Lokale wet- en regelgeving",
                    "section": link["title"],
                    "url": detail_url,
                }],
            })
        return {
            "source": "CVDR/SRU",
            "status": "ok" if records else "degraded",
            "checked_url": checked_url,
            "records": records,
            "count": len(records),
        }

    def live_smoke(self) -> dict:
        result = self.live_search(postcode="1011", product="evenement", limit=3)
        return {
            "source": "CVDR/SRU",
            "status": result["status"],
            "checked_url": result["checked_url"],
            "count": result["count"],
        }

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
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "CVDR/SRU", "status": "ok", "http_code": resp.status, "checked_url": CVDR_PAGE}
        except Exception as e:
            return {"source": "CVDR/SRU", "status": "error", "error": str(e)}
