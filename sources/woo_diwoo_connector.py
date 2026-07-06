"""Woo-index/DiWoo connector for publication metadata preflights."""
import html
from html.parser import HTMLParser
import json
import re
from urllib.parse import urlencode, urljoin
import urllib.request

from sources.base import BaseConnector

WOO_INDEX_PAGE = "https://organisaties.overheid.nl/woo"
WOO_SEARCH = "https://organisaties.overheid.nl/woo/zoeken"
USER_AGENT = "JuraRegel source-health/2026.1"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


class _AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self._href = ""
        self._text = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self._href = dict(attrs).get("href", "")
            self._text = []

    def handle_data(self, data):
        if self._href:
            self._text.append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self._href:
            text = html.unescape(" ".join("".join(self._text).split()))
            if text:
                self.links.append({"title": text, "href": self._href})
            self._href = ""
            self._text = []


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _categories(raw_html: str) -> list[str]:
    match = re.search(r"Gevonden informatie-categorie.n:\s*(.*?)</p>", raw_html or "", re.I | re.S)
    if not match:
        return []
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return [html.unescape(item.strip()) for item in text.split(",") if item.strip()]


class WooDiWooConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def lookup_organisation(
        self,
        organisatie: str,
        document_type: str = "",
        limit: int = 10,
        fetch_locations: bool = True,
    ) -> dict:
        params = {
            "keyword": organisatie,
            "maximumRecords": str(limit),
            "pageNumber": "1",
            "sortOrder": "0",
        }
        url = f"{WOO_SEARCH}?{urlencode(params)}"
        try:
            raw = _fetch(url)
        except Exception as exc:
            return {
                "source": "Woo-index/DiWoo",
                "status": "degraded",
                "error": str(exc),
                "checked_url": url,
                "documents": [],
                "count": 0,
            }
        result = self.parse_search_results(raw, checked_url=url, document_type=document_type, limit=limit)
        if fetch_locations:
            documents = []
            for org in result["organisations"]:
                try:
                    detail_html = _fetch(org["sourceUrl"])
                    documents.extend(self.parse_publication_locations(detail_html, org, document_type))
                except Exception as exc:
                    documents.append(self._document_from_org(org, document_type, error=str(exc)))
            result["documents"] = documents
            result["count"] = len(documents)
        return result

    def parse_search_results(
        self,
        raw_html: str,
        checked_url: str = WOO_SEARCH,
        document_type: str = "",
        limit: int = 10,
    ) -> dict:
        parser = _AnchorParser()
        parser.feed(raw_html or "")
        organisations = []
        seen = set()
        for link in parser.links:
            match = re.match(r"^/woo/(\d+)/([^/#?]+)$", link["href"])
            if not match or match.group(1) in seen:
                continue
            seen.add(match.group(1))
            organisations.append({
                "organisatie": _norm(link["title"]),
                "organisatieLabel": link["title"],
                "organisatieId": match.group(1),
                "tooiCode": "",
                "sourceUrl": urljoin(WOO_INDEX_PAGE, link["href"]),
                "categories": _categories(raw_html),
            })
            if len(organisations) >= limit:
                break
        documents = [self._document_from_org(org, document_type) for org in organisations]
        return {
            "source": "Woo-index/DiWoo",
            "status": "ok" if organisations else "degraded",
            "checked_url": checked_url,
            "organisations": organisations,
            "documents": documents,
            "count": len(documents),
        }

    def parse_publication_locations(
        self,
        raw_html: str,
        org: dict,
        document_type: str = "",
    ) -> list[dict]:
        start = (raw_html or "").find("locaties-woo-documenten")
        scoped = raw_html[start:] if start >= 0 else raw_html
        parser = _AnchorParser()
        parser.feed(scoped or "")
        docs = []
        wanted = _norm(document_type)
        for link in parser.links:
            if not link["href"].startswith("http"):
                continue
            doc_type = _norm(link["title"])
            if wanted and wanted not in doc_type and doc_type not in wanted:
                continue
            docs.append(self._document_from_org(org, doc_type or document_type, source_url=link["href"]))
        return docs or [self._document_from_org(org, document_type)]

    def _document_from_org(
        self,
        org: dict,
        document_type: str = "",
        source_url: str = "",
        error: str = "",
    ) -> dict:
        doc_type = _norm(document_type)
        metadata = {
            "tooiCode": org.get("tooiCode", ""),
            "organisatieId": org.get("organisatieId", ""),
            "documentType": doc_type,
            "publishedAt": "",
            "sourceUrl": source_url or org.get("sourceUrl", ""),
        }
        if error:
            metadata["fetchError"] = error
        return {
            "organisatie": org.get("organisatie", ""),
            "organisatieLabel": org.get("organisatieLabel", ""),
            "tooiCode": org.get("tooiCode", ""),
            "organisatieId": org.get("organisatieId", ""),
            "documentType": doc_type,
            "documentTypeLabel": document_type,
            "location": source_url or org.get("sourceUrl", ""),
            "metadata": metadata,
            "sourceRefs": [{
                "type": "regeling",
                "title": "Woo-index",
                "section": org.get("organisatieLabel", ""),
                "url": org.get("sourceUrl", WOO_INDEX_PAGE),
            }],
        }

    def live_smoke(self) -> dict:
        result = self.lookup_organisation("Amsterdam", limit=5, fetch_locations=False)
        return {
            "source": "Woo-index/DiWoo",
            "status": result["status"],
            "checked_url": result["checked_url"],
            "count": result["count"],
        }

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
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "Woo-index/DiWoo", "status": "ok", "http_code": resp.status, "checked_url": WOO_INDEX_PAGE}
        except Exception as e:
            return {"source": "Woo-index/DiWoo", "status": "error", "error": str(e)}
