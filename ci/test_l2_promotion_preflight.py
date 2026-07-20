import json
from pathlib import Path

from ci import l2_promotion_preflight as preflight


def write_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def valid_jrem(maturity="L1-poc", metadata=None, approval=None):
    return {
        "ruleSetId": "sample-ruleset",
        "version": "2026.1",
        "maturityLevel": maturity,
        "metadata": metadata or {"acceptatieType": "draft"},
        "approval": approval or {"type": "self"},
        "rules": [],
    }


def valid_template():
    return {
        "ruleSetId": "sample-ruleset",
        "version": "2026.1",
        "maturityTarget": "L2-pilot",
        "reviewer": {
            "geaccondeerdDoor": "Test Jurist",
            "rol": "juridisch eigenaar",
            "organisatie": "Testorganisatie",
        },
        "review": {
            "datum": "2026-07-07",
            "geldigTot": "2099-12-31",
            "scope": "L2 pilot scope",
            "bronSnapshot": "source-set-2026-07-07",
            "verklaring": "Akkoord binnen scope.",
            "beperkingen": ["Niet buiten scope gebruiken"],
        },
        "sourceSnapshotRefs": [
            {
                "name": "Bron",
                "url": "https://example.test/source",
                "checkedAt": "2026-07-07",
            }
        ],
        "scenarioAcceptance": [
            {"scenario": "Happy path", "accepted": True},
            {"scenario": "Manual review path", "accepted": True},
        ],
    }


def write_target(tmp_path, jrem, template):
    target = {
        "ruleSetId": "sample-ruleset",
        "jrem": "use-cases/sample/jrem/exports/sample.json",
        "template": "docs/acceptance-templates/sample.acceptance.json",
    }
    write_json(tmp_path / target["jrem"], jrem)
    write_json(tmp_path / target["template"], template)
    return target


def test_placeholder_template_is_not_ready_but_not_blocking(tmp_path):
    template = valid_template()
    template["reviewer"]["geaccondeerdDoor"] = "__JURIST_NAAM__"
    target = write_target(tmp_path, valid_jrem(), template)

    result = preflight.evaluate_target(tmp_path, target)

    assert result["templateStatus"] == "template-ready"
    assert result["ready"] is False
    assert result["blocking"] is False
    assert "template bevat placeholders" in result["reasons"]


def test_missing_source_snapshot_ref_is_reported(tmp_path):
    template = valid_template()
    template["sourceSnapshotRefs"] = []
    target = write_target(tmp_path, valid_jrem(), template)

    result = preflight.evaluate_target(tmp_path, target)

    assert result["ready"] is False
    assert "sourceSnapshotRefs ontbreekt" in result["reasons"]


def test_filled_template_can_be_ready_for_l2_review(tmp_path):
    target = write_target(tmp_path, valid_jrem(), valid_template())

    result = preflight.evaluate_target(tmp_path, target)

    assert result["ready"] is True
    assert result["blocking"] is False
    assert result["reasons"] == []


def test_filled_template_with_source_debt_is_not_ready(tmp_path):
    jrem = valid_jrem()
    jrem["rules"] = [{
        "ruleId": "R-1",
        "sourceRefs": [{
            "type": "standaard",
            "title": "Bron",
            "section": "paragraaf 1",
            "url": "https://example.test/source",
        }],
    }]
    target = write_target(tmp_path, jrem, valid_template())

    result = preflight.evaluate_target(tmp_path, target)

    assert result["ready"] is False
    assert "1 source-quality issue(s)" in result["reasons"]


def test_expired_l2_jrem_acceptance_blocks(tmp_path):
    accordering = preflight.template_accordering(valid_template())
    accordering["geldigTot"] = "2020-01-01"
    metadata = {"acceptatieType": "full", "juristAccordering": accordering}
    target = write_target(
        tmp_path,
        valid_jrem(maturity="L2-pilot", metadata=metadata, approval={"type": "jurist"}),
        valid_template(),
    )

    result = preflight.evaluate_target(tmp_path, target)

    assert result["blocking"] is True
    assert any("Acceptatie verlopen" in reason for reason in result["reasons"])


def test_template_version_mismatch_is_not_ready(tmp_path):
    template = valid_template()
    template["version"] = "2025.1"
    target = write_target(tmp_path, valid_jrem(), template)

    result = preflight.evaluate_target(tmp_path, target)

    assert result["ready"] is False
    assert any("komt niet overeen" in reason for reason in result["reasons"])
