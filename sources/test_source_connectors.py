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


def test_woo_diwoo_normalizes_documents_with_tooi_metadata():
    raw = (FIXTURES / "woo-diwoo.sample.json").read_text()
    documents = WooDiWooConnector().normalize(raw)["documents"]

    beschikking = next(d for d in documents if d["documentType"] == "beschikking")
    assert beschikking["organisatie"] == "gemeente amsterdam"
    assert beschikking["tooiCode"] == "gm0363"
    assert beschikking["metadata"]["publishedAt"] == "2026-07-01"


def test_sttr_rtr_normalizes_packages_with_jrem_mapping():
    raw = (FIXTURES / "sttr-rtr.sample.json").read_text()
    packages = STTRRTRConnector().normalize(raw)["packages"]

    valid = next(p for p in packages if p["packageId"] == "evenement-melding-amsterdam")
    assert valid["sttrVersion"] == "3.0.1"
    assert valid["jremMapping"]["mappedRuleIds"] == ["DRC-001", "DRC-002", "DRC-006"]


def test_connector_fixture_json_is_valid():
    json.loads((FIXTURES / "upl-actueel.sample.json").read_text())
    json.loads((FIXTURES / "tooi-roo.sample.json").read_text())
    json.loads((FIXTURES / "cvdr-sru.sample.json").read_text())
    json.loads((FIXTURES / "woo-diwoo.sample.json").read_text())
    json.loads((FIXTURES / "sttr-rtr.sample.json").read_text())
