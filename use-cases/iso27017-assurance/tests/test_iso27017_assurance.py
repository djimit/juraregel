import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
USE_CASE = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "evidence_assess",
    ROOT / "use-cases" / "acict-assurance" / "assess.py",
)
assess = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assess)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def keys(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys(item)}
    return set()


def test_profile_is_four_control_non_scoring_and_falsifiable():
    profile = load(USE_CASE / "profiles" / "iso27017-2026.json")

    assert [item["aspectId"] for item in profile["aspects"]] == [
        "iso27017-2026.5.38",
        "iso27017-2026.5.39",
        "iso27017-2026.8.35",
        "iso27017-2026.8.36",
    ]
    assert "score" not in keys(profile)
    mapping_ids = {
        mapping["mappingId"]
        for mapping in load(USE_CASE / "mappings" / "crosswalk-2026.json")["mappings"]
    }
    for aspect in profile["aspects"]:
        assert aspect["interpretationStatus"] == "local-non-normative"
        assert aspect["subject"]
        assert aspect["scope"]
        assert aspect["applicableCloudRoles"]
        assert aspect["artifactMetadataRequired"]
        assert set(aspect["mappingRefs"]) <= mapping_ids
        assert aspect["evidenceRequired"]
        assert aspect["falsifiedBy"]
        assert aspect["prohibitedInference"]


def test_source_and_crosswalk_boundaries_are_explicit():
    register = load(USE_CASE / "sources" / "source-register.json")
    profile = load(USE_CASE / "profiles" / "iso27017-2026.json")
    crosswalk = load(USE_CASE / "mappings" / "crosswalk-2026.json")
    source_ids = {item["sourceId"] for item in register["sources"]}
    control_ids = {item["aspectId"] for item in profile["aspects"]}

    assert register["licensedTextAvailable"] is False
    iso = next(item for item in register["sources"] if item["sourceId"] == "iso-27017-2026-catalogue")
    assert iso["publicationDate"] == "2026-07-27"
    assert iso["url"] == "https://www.iso.org/standard/27017"

    allowed = set(crosswalk["allowedRelationTypes"])
    mapping_ids = [mapping["mappingId"] for mapping in crosswalk["mappings"]]
    assert len(mapping_ids) == len(set(mapping_ids))
    assert crosswalk["reviewStatus"] == "draft"
    for mapping in crosswalk["mappings"]:
        assert mapping["sourceControl"] in control_ids
        assert mapping["relationType"] in allowed
        assert mapping["rationale"]
        source_ref = mapping["sourceRef"]
        if source_ref.startswith("local:"):
            assert (ROOT / source_ref.removeprefix("local:")).exists()
        else:
            assert source_ref in source_ids


def test_juraregel_assessment_fails_closed():
    profile = load(USE_CASE / "profiles" / "iso27017-2026.json")
    assessment = load(USE_CASE / "assessments" / "juraregel-2026.json")
    result = assess.evaluate(profile, assessment)

    assert result["status"] == "evidence-incomplete"
    assert result["aspectCount"] == 4
    assert result["incompleteAspects"] == [
        "iso27017-2026.5.38",
        "iso27017-2026.5.39",
        "iso27017-2026.8.35",
        "iso27017-2026.8.36",
    ]

    for finding in assessment["findings"]:
        finding["reviewedBy"] = "independent-reviewer"
        finding["reviewedAt"] = "2026-07-30"
    assert assess.evaluate(profile, assessment)["status"] == "evidence-incomplete"


def test_iso27002_source_anchors_are_reproducible():
    iso27002 = load(ROOT / "use-cases" / "iso27002" / "jrem" / "exports" / "iso27002-2026.1.json")
    for rule in iso27002["rules"]:
        for source in rule["sourceRefs"]:
            assert source["url"] == "https://www.iso.org/standard/75652"
            assert source["bronVersie"] == "2022-02"

    bio2 = load(ROOT / "use-cases" / "bio2" / "jrem" / "exports" / "bio2-maatregelen-2025.1.json")
    iso_sources = [
        source
        for rule in bio2["rules"]
        for source in rule["sourceRefs"]
        if source["title"] == "NEN-EN-ISO/IEC 27002"
    ]
    assert len(iso_sources) == 162
    assert all(source["type"] == "standaard" for source in iso_sources)
    assert all(source["url"] == "https://www.iso.org/standard/75652" for source in iso_sources)
    assert all(source["bronVersie"] == "2022-02" for source in iso_sources)


def test_iso27002_api_does_not_infer_compliance_percentage():
    source = (ROOT / "use-cases" / "iso27002" / "api" / "app.py").read_text()
    assert "~85%" not in source
    assert "impliceert geen ISO 27002-conformiteit" in source
    assert '"status": "insufficient_evidence"' in source
