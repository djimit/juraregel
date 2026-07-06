import json
from pathlib import Path

from sources.cvdr_sru_connector import CVDRSRUConnector
from sources.sttr_rtr_connector import STTRRTRConnector
from sources.tooi_roo_connector import TOOIROOConnector
from sources.upl_connector import UPLConnector
from sources.woo_diwoo_connector import WooDiWooConnector

FIXTURES = Path(__file__).parent / "fixtures"


def test_upl_normalizes_products_with_layers_and_source_refs():
    raw = (FIXTURES / "upl-actueel.sample.json").read_text()
    products = UPLConnector().normalize(raw)["products"]

    event = next(p for p in products if p["name"] == "evenementenvergunning")
    assert event["bestuurslagen"] == ["gemeente"]
    assert event["signals"]["sdg"] is True
    assert event["signals"]["aanvraag"] is True
    assert event["sourceRefs"][0]["title"] == "Uniforme Productnamenlijst (UPL)"


def test_tooi_roo_normalizes_organisations_with_layers_and_source_refs():
    raw = (FIXTURES / "tooi-roo.sample.json").read_text()
    organisations = TOOIROOConnector().normalize(raw)["organisations"]

    amsterdam = next(o for o in organisations if o["code"] == "gm0363")
    ministry = next(o for o in organisations if o["code"] == "mnre1034")
    assert amsterdam["bestuurslaag"] == "gemeente"
    assert amsterdam["officialName"] == "gemeente Amsterdam"
    assert ministry["bestuurslaag"] == "rijk"
    assert ministry["sourceRefs"][0]["title"] == "TOOI/ROO waardelijst"


def test_cvdr_sru_normalizes_local_regulation_records():
    raw = (FIXTURES / "cvdr-sru.sample.json").read_text()
    records = CVDRSRUConnector().normalize(raw)["records"]

    event = next(r for r in records if r["product"] == "evenementenvergunning")
    assert event["postcode"] == "1011ab"
    assert event["bestuurslaag"] == "gemeente"
    assert event["bevoegdGezag"] == "gemeente Amsterdam"
    assert event["sourceRefs"][0]["title"] == "Lokale wet- en regelgeving"


def test_cvdr_live_parser_normalizes_result_links_with_source_refs():
    raw = """
    <h1 class="h1 h1--slim">Zoekresultaten <span>1-2 van de 2 resultaten</span></h1>
    <h2 class="result--title"><a href="/CVDR696291/15">Omgevingsplan gemeente Amsterdam</a></h2>
    <h2 class="result--title"><a href="/CVDR761824/1">Subsidieregeling Evenementenfonds Amsterdam</a></h2>
    """

    result = CVDRSRUConnector().parse_live_results(
        raw,
        checked_url="https://lokaleregelgeving.overheid.nl/ZoekResultaat?locatie=1011",
        postcode="1011 AB",
        product="evenement",
        bestuursorgaan="gemeente Amsterdam",
        bestuurslaag="gemeente",
    )

    assert result["status"] == "ok"
    assert result["count"] == 2
    assert result["records"][0]["postcode"] == "1011ab"
    assert result["records"][0]["product"] == "evenement"
    assert result["records"][0]["bestuurslaag"] == "gemeente"
    assert result["records"][0]["bevoegdGezag"] == "gemeente Amsterdam"
    assert result["records"][0]["sourceRefs"][0]["url"].endswith("/CVDR696291/15")


def test_cvdr_live_parser_marks_empty_results_degraded():
    result = CVDRSRUConnector().parse_live_results("<h1>Zoekresultaten 0</h1>", postcode="9999")

    assert result["status"] == "degraded"
    assert result["records"] == []


def test_cvdr_live_search_builds_postcode_query(monkeypatch):
    captured = {}

    def fake_fetch(url):
        captured["url"] = url
        return '<h2 class="result--title"><a href="/CVDR1/1">Testregeling</a></h2>'

    monkeypatch.setattr("sources.cvdr_sru_connector._fetch", fake_fetch)

    result = CVDRSRUConnector().live_search(postcode="1011 AB", product="evenement")

    assert "locatie=1011" in captured["url"]
    assert "tekst=evenement" in captured["url"]
    assert result["count"] == 1


def test_woo_diwoo_normalizes_documents_with_tooi_metadata():
    raw = (FIXTURES / "woo-diwoo.sample.json").read_text()
    documents = WooDiWooConnector().normalize(raw)["documents"]

    beschikking = next(d for d in documents if d["documentType"] == "beschikking")
    assert beschikking["organisatie"] == "gemeente amsterdam"
    assert beschikking["tooiCode"] == "gm0363"
    assert beschikking["metadata"]["publishedAt"] == "2026-07-01"


def test_woo_live_search_parser_extracts_organisation_and_categories():
    raw = """
    <p>Gevonden informatie-categorieën: beschikkingen, convenanten</p>
    <h2 class="result--title"><a href="/woo/25698/Gemeente_Amsterdam">Gemeente Amsterdam</a></h2>
    """

    result = WooDiWooConnector().parse_search_results(raw, document_type="beschikkingen")

    assert result["status"] == "ok"
    assert result["organisations"][0]["organisatieId"] == "25698"
    assert result["organisations"][0]["organisatie"] == "gemeente amsterdam"
    assert "beschikkingen" in result["organisations"][0]["categories"]
    assert result["documents"][0]["metadata"]["sourceUrl"].endswith("/woo/25698/Gemeente_Amsterdam")


def test_woo_publication_location_parser_does_not_fetch_document_bodies():
    org = {
        "organisatie": "gemeente amsterdam",
        "organisatieLabel": "Gemeente Amsterdam",
        "organisatieId": "25698",
        "tooiCode": "gm0363",
        "sourceUrl": "https://organisaties.overheid.nl/woo/25698/Gemeente_Amsterdam",
    }
    raw = """
    <section id="locaties-woo-documenten">
      <a href="https://zoek.officielebekendmakingen.nl/resultaten?q=beschikking">Beschikkingen</a>
      <a href="https://open.amsterdam/convenanten">Convenanten</a>
    </section>
    """

    docs = WooDiWooConnector().parse_publication_locations(raw, org, "beschikking")

    assert len(docs) == 1
    assert docs[0]["documentType"] == "beschikkingen"
    assert docs[0]["metadata"]["tooiCode"] == "gm0363"
    assert docs[0]["metadata"]["sourceUrl"].startswith("https://zoek.officielebekendmakingen.nl/")


def test_woo_live_parser_marks_missing_organisation_degraded():
    result = WooDiWooConnector().parse_search_results("<h1>Geen resultaat</h1>")

    assert result["status"] == "degraded"
    assert result["documents"] == []


def test_sttr_rtr_normalizes_packages_with_jrem_mapping():
    raw = (FIXTURES / "sttr-rtr.sample.json").read_text()
    packages = STTRRTRConnector().normalize(raw)["packages"]

    valid = next(p for p in packages if p["packageId"] == "evenement-melding-amsterdam")
    assert valid["sttrVersion"] == "3.0.1"
    assert valid["jremMapping"]["mappedRuleIds"] == ["DRC-001", "DRC-002", "DRC-006"]


def test_sttr_supported_version_parser_reads_iplo_versions():
    raw = """
    <p>Het DSO ondersteunt de volgende versies van de STTR:</p>
    <li>Versie 3.0: beschikbaar vanaf 1 juli 2025</li>
    <li>Versie 2.0: beschikbaar vanaf 16 augustus 2023</li>
    <li>Versie 1.5: beschikbaar vanaf 16 augustus 2023</li>
    """

    result = STTRRTRConnector().parse_supported_versions(raw)

    assert result["status"] == "ok"
    assert result["supportedVersions"][:3] == ["3.0", "2.0", "1.5"]
    assert result["latest"] == "3.0"


def test_sttr_xml_package_metadata_parser_maps_versions_and_rules():
    raw = """
    <package id="evenement-melding-amsterdam">
      <sttrVersion>3.0.1</sttrVersion>
      <imtrVersion>3.0.1</imtrVersion>
      <rtrVersion>2026.1</rtrVersion>
      <mappedRuleId>DRC-001</mappedRuleId>
      <mappedRuleId>DRC-002</mappedRuleId>
    </package>
    """

    package = STTRRTRConnector().parse_package_metadata(raw)["packages"][0]

    assert package["packageId"] == "evenement-melding-amsterdam"
    assert package["sttrVersion"] == "3.0.1"
    assert package["imtrVersion"] == "3.0.1"
    assert package["rtrVersion"] == "2026.1"
    assert package["jremMapping"]["mappedRuleIds"] == ["DRC-001", "DRC-002"]


def test_connector_fixture_json_is_valid():
    json.loads((FIXTURES / "upl-actueel.sample.json").read_text())
    json.loads((FIXTURES / "tooi-roo.sample.json").read_text())
    json.loads((FIXTURES / "cvdr-sru.sample.json").read_text())
    json.loads((FIXTURES / "woo-diwoo.sample.json").read_text())
    json.loads((FIXTURES / "sttr-rtr.sample.json").read_text())
