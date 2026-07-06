import json
from pathlib import Path

from sources.tooi_roo_connector import TOOIROOConnector
from sources.upl_connector import UPLConnector

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


def test_connector_fixture_json_is_valid():
    json.loads((FIXTURES / "upl-actueel.sample.json").read_text())
    json.loads((FIXTURES / "tooi-roo.sample.json").read_text())
