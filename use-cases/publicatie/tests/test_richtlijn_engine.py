import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "lib"))
from richtlijn_engine_v4 import (
    PersoonType,
    PseudonimiseringsStatus,
    apply_richtlijn_v4,
    scan_met_richtlijn_v4,
)


def decision(text: str, match: str, given_type: str = "street_address"):
    start = text.index(match)
    return apply_richtlijn_v4(given_type, match, start, start + len(match), text)


def test_private_home_address_is_pseudonymised():
    result = decision("Eiser woont aan Dorpsstraat 12.", "Dorpsstraat 12")
    assert result.persoon_type == PersoonType.PARTICULAR
    assert result.status == PseudonimiseringsStatus.PSEUDONIMISEER


def test_professional_address_is_not_pseudonymised():
    result = decision("De advocaat werkt aan Dorpsstraat 12.", "Dorpsstraat 12")
    assert result.persoon_type == PersoonType.PROFESSIONAL
    assert result.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER


def test_offline_scanner_detects_and_classifies_email():
    result = scan_met_richtlijn_v4("Eiser gebruikt burger@example.nl")
    assert result.totaal_gedetecteerd == 1
    assert result.decisions[0].gegeven_type == "email"
    assert "evaluation pending" in result.accuracy_notes
