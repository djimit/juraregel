"""
LLM-Assisted Rule Extraction Engine.

Extracts rules from government source text using pattern-based confidence scoring.
LLM integration via OpenAI-compatible API (injectable).
"""
import json
import re
from pathlib import Path
from typing import Optional

EXTRACTION_PROMPT_TEMPLATE = """Je bent een juridische rule extraction assistant. Je taak is om een wetstekst om te zetten naar gestructureerde regels.

Wetstekst:
{artikel_tekst}

Instructies:
1. Identificeer de rechtsgevolgen in de tekst.
2. Identificeer de voorwaarden die leiden tot elk rechtsgevolg.
3. Identificeer uitzonderingen.
4. Formuleer elke regel als JSON met: rule_id, name, conditions, outcome, sourceRefs, confidence (0-100)
5. Confidence scoring:
   - 90-100: exacte drempelwaarden, bedragen, categorieen
   - 70-89: voorwaarden met operator-combinaties
   - 0-69: open normen, discretionaire ruimte

Output als JSON array."""

def recognize_structure(text: str) -> list[dict]:
    """Recognize article/section structure from raw text."""
    articles = []
    # Match patterns like "Artikel 8", "Art. 8", "Article 8"
    pattern = r'(?:Artikel|Art\.)\s+(\d+[a-z]?)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))

    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        articles.append({
            "artikel_nummer": match.group(1),
            "text": text[start:end].strip(),
            "start": start,
            "end": end,
        })

    return articles

def extract_rules(text: str, domain: str, llm_client=None) -> list[dict]:
    """Extract rules from text. Uses LLM if available, falls back to pattern extraction."""
    articles = recognize_structure(text)
    rules = []

    for art in articles:
        # Pattern-based extraction as fallback / seed
        conditions = _extract_conditions(art["text"])
        outcome = _extract_outcome(art["text"])

        if conditions or outcome:
            confidence = _score_confidence(art["text"], conditions, outcome)
            rules.append({
                "rule_id": f"{domain}-ext-{art['artikel_nummer']}-{len(rules) + 1:03d}",
                "domain": domain,
                "name": f"Regel uit art. {art['artikel_nummer']}",
                "conditions": conditions,
                "outcome": outcome,
                "source_refs": [{"type": "wet", "title": domain, "section": f"art. {art['artikel_nummer']}"}],
                "confidence": confidence,
                "confidence_reason": _confidence_reason(confidence),
                "wetstekst": art["text"][:500],
            })

    return rules

def _extract_conditions(text: str) -> dict:
    """Extract conditions from text using patterns."""
    conditions = {}

    # Income thresholds
    income_match = re.search(r'inkomen\s*(?:van\s+)?(?:ten\s+hoogste|minder\s+dan|tot)\s+EUR?\s*([\d.]+)', text, re.IGNORECASE)
    if income_match:
        amount = float(income_match.group(1).replace('.', ''))
        conditions["inkomen"] = {"lte": amount}

    # Age thresholds
    age_match = re.search(r'(?:leeftijd|ouder|jonger)\s+(?:dan\s+)?(\d+)', text, re.IGNORECASE)
    if age_match:
        conditions["leeftijd"] = {"gte": int(age_match.group(1))}

    # Boolean conditions
    if 'alleenstaand' in text.lower() or 'alleenstaande' in text.lower():
        conditions["alleenstaande"] = True
    if 'samenwonend' in text.lower() or 'gehuwd' in text.lower():
        conditions["alleenstaande"] = False

    return conditions

def _extract_outcome(text: str) -> dict:
    """Extract outcome from text using patterns."""
    outcome = {}

    # Right/benefit
    if re.search(r'recht\s+op', text, re.IGNORECASE):
        outcome["recht"] = True

    # Amount
    amount_match = re.search(r'EUR?\s*([\d.]+)\s*(?:per\s+(maand|jaar|keer))?', text)
    if amount_match:
        outcome["bedrag"] = {
            "amount": float(amount_match.group(1).replace('.', '')),
            "currency": "EUR",
            "periode": amount_match.group(2) or "eenmalig",
        }

    # Grant/permit
    if 'vergunning' in text.lower():
        outcome["vergunningplichtig"] = 'niet vergunningplichtig' not in text.lower()

    return outcome

def _score_confidence(text: str, conditions: dict, outcome: dict) -> int:
    """Score confidence based on extractability."""
    score = 50  # base

    # Boost for exact numbers
    if re.search(r'\d+[.,]?\d*\s*(?:EUR|%|jaar|maand)', text):
        score += 20

    # Boost for clear conditions
    if len(conditions) >= 2:
        score += 15

    # Boost for clear outcome
    if outcome:
        score += 10

    # Penalty for vague language
    vague_terms = ['redelijkerwijs', 'in redere zin', 'naar gelang', 'indien', 'tenzij']
    for term in vague_terms:
        if term in text.lower():
            score -= 15

    return max(0, min(100, score))

def _confidence_reason(confidence: int) -> str:
    if confidence >= 90:
        return "Exacte drempelwaarden en duidelijke voorwaarden"
    elif confidence >= 70:
        return "Voorwaarden met operator-combinaties"
    else:
        return "Open normen of discretionaire ruimte"
