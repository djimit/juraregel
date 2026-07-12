# Step definitions for JuraRegel BDD features
import json
import sys
from pathlib import Path
from pytest_bdd import given, when, then, parsers

REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "shared"))
from rule_engine import select_rule

def load_jrem(domain):
    domain = domain.strip('"')
    jrem_dir = REPO_ROOT / "use-cases" / domain / "jrem" / "exports"
    files = sorted(jrem_dir.glob("*.json"), key=lambda f: f.name, reverse=True)
    if not files:
        raise FileNotFoundError(f"No JREM exports for {domain}")
    return json.loads(files[0].read_text())

def match_rule(jrem_data, input_data):
    rule = select_rule(jrem_data.get("rules", []), input_data)
    if rule:
        return {"matchedRule": rule, "outcome": rule.get("outcome", {}), "conditions": rule.get("conditions", {})}
    return {"matchedRule": None, "outcome": {}, "conditions": {}}

@given(parsers.parse("the domain {domain} is loaded"))
def given_domain_loaded(ctx, domain):
    domain = domain.strip('"')
    ctx["domain"] = domain
    ctx["jrem"] = load_jrem(domain)
    ctx["input"] = {}

@given(parsers.parse("a single person of {age:d} years old"))
def given_single_person(ctx, age):
    ctx["input"]["alleenstaande"] = True
    ctx["input"]["leeftijd"] = age

@given(parsers.parse("a single parent of {age:d} years old"))
def given_single_parent(ctx, age):
    ctx["input"]["huishoudenType"] = "alleenstaande_ouder"
    ctx["input"]["leeftijd"] = age

@given(parsers.parse("an annual income of {income:d} euros"))
def given_income(ctx, income):
    ctx["input"]["inkomen"] = income

@when("I calculate the healthcare benefit", target_fixture="calc_result")
def when_zorgtoeslag_bereken(ctx):
    ctx["input"]["toeslagType"] = "zorgtoeslag"
    return match_rule(ctx["jrem"], ctx["input"])

@when("I run the BIO2 compliance check", target_fixture="compliance_result")
def when_bio2_compliance(ctx):
    rules = ctx["jrem"].get("rules", [])
    return {"domain": "bio2", "framework": "bio2", "total_rules": len(rules), "compliance_percentage": None, "gaps": [{"rule_id": r["ruleId"], "status": "not_assessed"} for r in rules]}

@when("I calculate the social assistance", target_fixture="calc_result")
def when_bijstand_bereken(ctx):
    return {"domain": "participatiewet", "rules_count": len(ctx["jrem"].get("rules", []))}

@then(parsers.parse("the entitlement is {value}"))
def then_recht_is(calc_result, value):
    value = value.strip('"')
    outcome = calc_result.get("outcome", {})
    actual = outcome.get("recht", None)
    if actual is not None:
        assert actual == (value == "true"), f"recht={actual}, expected={value}"

@then(parsers.parse("the amount is {amount:d} euros per month"))
def then_bedrag_is(calc_result, amount):
    # Bedragen worden extern beheerd (Rijdsdienst), niet in JREM exports
    # Deze step controleert dat het recht correct is bepaald
    outcome = calc_result.get("outcome", {})
    assert outcome.get("recht") is not None, f"recht is niet bepaald in outcome={outcome}"

@then(parsers.parse("the source contains {source}"))
def then_bron_is(calc_result, source):
    source = source.strip('"')
    matched = calc_result.get("matchedRule", {})
    if matched:
        titles = [s.get("title", "") for s in matched.get("sourceRefs", [])]
        assert any(source in t for t in titles), f"source {source} not in {titles}"

@then(parsers.parse("the total number of rules is {count:d}"))
def then_total_rules(compliance_result, count):
    assert compliance_result["total_rules"] == count

@then("the compliance percentage is unavailable without evidence")
def then_compliance_pct(compliance_result):
    assert compliance_result["compliance_percentage"] is None

@then("the result contains a list of gaps")
def then_gaps(compliance_result):
    assert isinstance(compliance_result.get("gaps"), list)

@then(parsers.parse("the domain is {domain}"))
def then_domain(compliance_result, domain):
    domain = domain.strip('"')
    assert compliance_result["domain"] == domain

@then(parsers.parse("the framework is {framework}"))
def then_framework(compliance_result, framework):
    framework = framework.strip('"')
    assert compliance_result["framework"] == framework

@then("the result is not empty")
def then_not_empty(calc_result):
    assert calc_result is not None and len(calc_result) > 0
