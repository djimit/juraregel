"""STTR/IMTR + RTR connector for applicable-rule package preflights."""
import json
import re
import xml.etree.ElementTree as ET
import urllib.request

from sources.base import BaseConnector

STTR_PAGE = "https://iplo.nl/digitaal-stelsel/aansluiten/standaarden/sttr-imtr/"
USER_AGENT = "JuraRegel source-health/2026.1"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


class STTRRTRConnector(BaseConnector):
    def list_sources(self) -> list[dict]:
        return []

    def get_document(self, doc_id: str) -> dict:
        return {"error": "not_implemented", "doc_id": doc_id}

    def check_for_updates(self, last_check: str = None) -> list[dict]:
        return []

    def fetch_supported_versions(self) -> dict:
        try:
            raw = _fetch(STTR_PAGE)
        except Exception as exc:
            return {
                "source": "STTR/IMTR+RTR",
                "status": "degraded",
                "error": str(exc),
                "checked_url": STTR_PAGE,
                "supportedVersions": [],
            }
        return self.parse_supported_versions(raw)

    def parse_supported_versions(self, raw_html: str) -> dict:
        scoped = raw_html or ""
        start = scoped.find("Het DSO ondersteunt de volgende versies")
        if start >= 0:
            scoped = scoped[start:]
        end = scoped.find("Afspraken over ondersteunen")
        if end >= 0:
            scoped = scoped[:end]
        versions = []
        for version in re.findall(r"Versie\s+(\d+\.\d+)", scoped, re.I):
            if version not in versions:
                versions.append(version)
        return {
            "source": "STTR/IMTR+RTR",
            "status": "ok" if versions else "degraded",
            "checked_url": STTR_PAGE,
            "supportedVersions": versions,
            "latest": versions[0] if versions else "",
            "sourceRefs": [{
                "type": "standaard",
                "title": "STTR/IMTR",
                "section": "Status beschikbare versies STTR en IMTR",
                "url": STTR_PAGE,
            }],
        }

    def parse_package_metadata(self, raw_data: str) -> dict:
        raw = (raw_data or "").strip()
        if raw.startswith("{"):
            return self.normalize(raw)
        root = ET.fromstring(raw)
        values = {}
        mapped_rule_ids = []
        for elem in root.iter():
            name = _local_name(elem.tag)
            text = (elem.text or "").strip()
            if name in {"packageId", "sttrVersion", "imtrVersion", "rtrVersion", "status"} and text:
                values[name] = text
            elif name in {"mappedRuleId", "ruleId"} and text:
                mapped_rule_ids.append(text)
        if not values.get("packageId"):
            values["packageId"] = root.attrib.get("id", "")
        package = {
            "packageId": values.get("packageId", ""),
            "sttrVersion": values.get("sttrVersion", ""),
            "imtrVersion": values.get("imtrVersion", ""),
            "rtrVersion": values.get("rtrVersion", ""),
            "status": values.get("status", "metadata-only"),
            "issues": [],
            "jremMapping": {"mappedRuleIds": mapped_rule_ids},
            "sourceRefs": [{
                "type": "standaard",
                "title": "STTR/IMTR",
                "section": "Package metadata",
                "url": STTR_PAGE,
            }],
        }
        return self.normalize(json.dumps({"packages": [package]}))

    def live_smoke(self) -> dict:
        result = self.fetch_supported_versions()
        return {
            "source": "STTR/IMTR+RTR",
            "status": result["status"],
            "checked_url": result["checked_url"],
            "supportedVersions": result.get("supportedVersions", []),
        }

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
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return {"source": "STTR/IMTR+RTR", "status": "ok", "http_code": resp.status, "checked_url": STTR_PAGE}
        except Exception as e:
            return {"source": "STTR/IMTR+RTR", "status": "error", "error": str(e)}
