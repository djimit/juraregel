import importlib.util
from pathlib import Path


path = Path(__file__).with_name("extractor.py")
spec = importlib.util.spec_from_file_location("rule_extractor", path)
extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extractor)


def test_pattern_extraction_detects_right_and_amount():
    rules = extractor.extract_rules(
        "Artikel 8 De alleenstaande heeft recht op EUR 100 per maand.", "test"
    )
    assert rules[0]["outcome"]["recht"] is True
    assert rules[0]["outcome"]["bedrag"]["amount"] == 100


def test_llm_proposal_is_always_pending_review():
    response = '[{"name":"Voorstel","conditions":{},"outcome":{"recht":true}}]'
    rules = extractor.extract_rules("Artikel 1 Tekst.", "test", llm_client=lambda _: response)
    assert rules[0]["review_status"] == "pending"
    assert rules[0]["interpretatieMethode"] == "LLM-assisteerd"
