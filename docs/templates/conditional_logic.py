"""Conditional Invul-Logic Engine — Fase 4: Tooling & Interoperabiliteit.

Ondersteunt conditionele secties in templates:
- Toon/verberg secties gebaseerd op eerdere antwoorden
- Automatische scoring en routing
- Afhankelijkheidsregels tussen secties

Gebruik:
    from docs.templates.conditional_logic import ConditionalForm
    form = ConditionalForm("dpia_pre_scan", "Gemeente Test")
    form.set_answer("stap_2.criteria.c1", "Ja")
    visible = form.get_visible_sections()
    next_questions = form.get_next_questions()
"""

from __future__ import annotations

from typing import Any

from . import generate_document


class ConditionalForm:
    """Interactief formulier met conditional logic over een template."""

    def __init__(self, doc_type: str, org_naam: str, **kwargs):
        self.doc_type = doc_type
        self.org_naam = org_naam
        defaults = {
            "verwerking": kwargs.get("verwerking", "[verwerking]"),
            "ai_systeem": kwargs.get("ai_systeem", "[AI-systeem]"),
            "systeem": kwargs.get("systeem", "[systeem]"),
            "belang": kwargs.get("belang", "[belang]"),
            "ontvanger_land": kwargs.get("ontvanger_land", "[land]"),
            "ontvanger_naam": kwargs.get("ontvanger_naam", "[ontvanger]"),
        }
        merged = {**defaults, **kwargs}
        self.template = generate_document(doc_type, org_naam, **merged)
        self.answers: dict[str, Any] = {}
        self._rules = self._build_rules()

    def _build_rules(self) -> list[dict]:
        """Bouw conditionele regels op basis van het document-type."""
        rules = []

        if self.doc_type == "dpia_pre_scan":
            rules = [
                {
                    "id": "stap_2_shown",
                    "condition": lambda a: a.get("stap_1.ap_lijst") == "Nee",
                    "show": ["stap_2"],
                    "hide": [],
                },
                {
                    "id": "stap_3_go",
                    "condition": lambda a: a.get("stap_2.positief_count", 0) >= 2,
                    "show": ["stap_3"],
                    "message": "GO: Volledige DPIA is verplicht",
                },
                {
                    "id": "stap_3_nogo",
                    "condition": lambda a: a.get("stap_2.positief_count", 0) < 2,
                    "show": ["stap_3"],
                    "message": "NO-GO: DPIA niet verplicht",
                },
            ]
        elif self.doc_type == "ai_risicoclassificatie":
            rules = [
                {
                    "id": "not_ai",
                    "condition": lambda a: a.get("stap_1.is_ai") == "Nee",
                    "show": [],
                    "hide": ["stap_2", "stap_3", "stap_4", "stap_5"],
                    "message": "EU AI Act niet van toepassing — geen AI-systeem",
                },
                {
                    "id": "verboden",
                    "condition": lambda a: a.get("stap_2.verboden") == "Ja",
                    "show": ["stap_5"],
                    "hide": ["stap_3", "stap_4"],
                    "message": "STOP: Systeem is verboden",
                },
                {
                    "id": "hoog_risico",
                    "condition": lambda a: a.get("stap_3.hoog_risico") == "Ja",
                    "show": ["stap_4", "stap_5"],
                    "message": "HOOG-RISICO: Alle verplichtingen van toepassing",
                },
            ]
        elif self.doc_type == "lia":
            rules = [
                {
                    "id": "purpose_failed",
                    "condition": lambda a: a.get("stap_1.purpose") == "Nee",
                    "show": ["eindoordeel"],
                    "hide": ["stap_2", "stap_3"],
                    "message": "Purpose test niet geslaagd — kies andere rechtsgrond",
                },
                {
                    "id": "necessity_failed",
                    "condition": lambda a: a.get("stap_2.necessity") == "Nee",
                    "show": ["stap_2"],
                    "hide": ["stap_3"],
                    "message": "Necessity test niet geslaagd — pas verwerking aan",
                },
                {
                    "id": "balancing_failed",
                    "condition": lambda a: a.get("stap_3.balancing") == "Nee",
                    "show": ["eindoordeel"],
                    "message": "Balancing test niet geslaagd — kies andere rechtsgrond",
                },
            ]

        return rules

    def set_answer(self, question_id: str, answer: Any) -> None:
        """Registreer een antwoord."""
        self.answers[question_id] = answer

    def get_visible_sections(self) -> list[str]:
        """Bepaal welke secties zichtbaar zijn op basis van antwoorden."""
        all_sections = list(self.template.get("inhoud", {}).keys())
        visible = set(all_sections)

        for rule in self._rules:
            if rule["condition"](self.answers):
                for s in rule.get("show", []):
                    visible.add(s)
                for s in rule.get("hide", []):
                    visible.discard(s)

        return [s for s in all_sections if s in visible]

    def get_next_questions(self) -> list[dict]:
        """Bepaal de volgende beantwoorde/vraag-secties."""
        visible = self.get_visible_sections()
        questions = []

        for section_id in visible:
            section = self.template.get("inhoud", {}).get(section_id, {})
            if isinstance(section, dict):
                title = section.get("titel", section_id)
                instructie = section.get("instructie", "")
                questions.append(
                    {
                        "id": section_id,
                        "title": title,
                        "instruction": instructie,
                        "answered": section_id in self.answers,
                    }
                )

        return questions

    def get_messages(self) -> list[str]:
        """Haal actieve conditie-berichten op."""
        messages = []
        for rule in self._rules:
            if rule["condition"](self.answers):
                msg = rule.get("message")
                if msg:
                    messages.append(msg)
        return messages

    def get_progress(self) -> dict:
        """Bereken voortgang."""
        visible = self.get_visible_sections()
        answered = [s for s in visible if s in self.answers]
        total = len(visible)
        done = len(answered)

        return {
            "total_sections": total,
            "answered": done,
            "remaining": total - done,
            "percent": round((done / total * 100) if total > 0 else 0),
        }


def evaluate_condition(answers: dict, condition_expr: str) -> bool:
    """Evalueer een eenvoudige conditie-expressie.

    Ondersteunt:
    - "key==value"
    - "key!=value"
    - "key>=number"
    - "key<=number"

    Voorbeeld:
        evaluate_condition({"score": 3}, "score>=2") → True
    """
    condition_expr = condition_expr.strip()

    for op in ["==", "!=", ">=", "<="]:
        if op in condition_expr:
            parts = condition_expr.split(op)
            if len(parts) == 2:
                key = parts[0].strip()
                expected = parts[1].strip()
                actual = answers.get(key)

                if actual is None:
                    return False

                if op == "==":
                    return str(actual) == expected
                elif op == "!=":
                    return str(actual) != expected
                elif op in (">=", "<="):
                    try:
                        return (
                            float(actual) >= float(expected)
                            if op == ">="
                            else float(actual) <= float(expected)
                        )
                    except (ValueError, TypeError):
                        return False

    return False
