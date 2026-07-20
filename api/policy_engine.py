"""Policy-as-Code Engine — Compliance rules as testable policies.

Encodes legal requirements as machine-readable, testable policies.
Supports Rego-like logic without external dependencies.

Policies:
- AVG Art. 25: Data Minimization
- AVG Art. 32: Security of Processing
- EU AI Act Art. 10: Data Governance
- EU AI Act Art. 14: Human Oversight
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ─── Policy Result ─────────────────────────────────────────────


class Severity(str, Enum):
    COMPLIANT = "compliant"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class PolicyViolation:
    """A single policy violation."""

    policy_id: str
    article: str
    message: str
    severity: Severity
    remediation: str
    citation: str


@dataclass
class PolicyResult:
    """Result of a policy evaluation."""

    policy_id: str
    compliant: bool
    violations: list[PolicyViolation] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)


# ─── Policy Base ───────────────────────────────────────────────


class Policy:
    """Base class for compliance policies."""

    def __init__(self, policy_id: str, article: str, description: str):
        self.policy_id = policy_id
        self.article = article
        self.description = description

    def evaluate(self, context: dict) -> PolicyResult:
        """Evaluate the policy against a context."""
        raise NotImplementedError


# ─── AVG Art. 25: Data Minimization ───────────────────────────


class DataMinimizationPolicy(Policy):
    """AVG Art. 25 — Data Minimization.

    Only personal data that is necessary for each specific purpose
    should be processed.
    """

    def __init__(self):
        super().__init__(
            policy_id="avg-art25-data-minimization",
            article="AVG Art. 25(1)",
            description="Data Minimization — alleen noodzakelijke gegevens verwerken",
        )

    def evaluate(self, context: dict) -> PolicyResult:
        purpose = context.get("purpose", "")
        data_categories = context.get("data_categories", [])
        necessary_fields = self._get_necessary_fields(purpose)
        excess_fields = [f for f in data_categories if f not in necessary_fields]

        if excess_fields:
            return PolicyResult(
                policy_id=self.policy_id,
                compliant=False,
                violations=[
                    PolicyViolation(
                        policy_id=self.policy_id,
                        article=self.article,
                        message=f"Excessieve gegevensverwerking gedetecteerd: {', '.join(excess_fields)}",
                        severity=Severity.HIGH,
                        remediation=f"Verwijder onnodige velden: {', '.join(excess_fields)}",
                        citation="AVG Art. 25(1), EDPB Guidelines 4/2019 §12",
                    )
                ],
            )

        return PolicyResult(
            policy_id=self.policy_id,
            compliant=True,
            evidence=[
                f"Alle {len(data_categories)} velden zijn noodzakelijk voor doel: {purpose}"
            ],
        )

    def _get_necessary_fields(self, purpose: str) -> list[str]:
        """Get necessary fields for a given purpose."""
        purpose_lower = purpose.lower()
        necessary = []

        if "woz" in purpose_lower or "waardering" in purpose_lower:
            necessary = ["Naam", "Adres", "WOZ-waarde", "Woninggegevens"]
        elif "recruitment" in purpose_lower or "sollicitatie" in purpose_lower:
            necessary = ["Naam", "Contactgegevens", "Opleiding", "Werkervaring"]
        elif "gezondheid" in purpose_lower or "zorg" in purpose_lower:
            necessary = ["Naam", "BSN", "Gezondheidsgegevens", "Verwijzing"]

        return necessary


# ─── AVG Art. 32: Security of Processing ─────────────────────


class SecurityPolicy(Policy):
    """AVG Art. 32 — Security of Processing.

    Appropriate technical and organizational measures to ensure security.
    """

    def __init__(self):
        super().__init__(
            policy_id="avg-art32-security",
            article="AVG Art. 32",
            description="Security of Processing — passende technische en organisatorische maatregelen",
        )

    def evaluate(self, context: dict) -> PolicyResult:
        violations = []
        measures = context.get("security_measures", [])
        data_categories = context.get("data_categories", [])

        # Check for encryption
        sensitive = {
            "biometrische gegevens",
            "gezondheidsgegevens",
            "strafrechtelijke gegevens",
        }
        has_sensitive = any(cat.lower() in sensitive for cat in data_categories)

        if has_sensitive:
            if "encryptie" not in str(measures).lower():
                violations.append(
                    PolicyViolation(
                        policy_id=self.policy_id,
                        article=self.article,
                        message="Gevoelige gegevens vereisen encryptie (at rest + in transit)",
                        severity=Severity.CRITICAL,
                        remediation="Implementeer AES-256 encryptie at rest en TLS 1.3 in transit",
                        citation="AVG Art. 32(1)(a), EDPB Guidelines 01/2025",
                    )
                )

            if "pseudonimisering" not in str(measures).lower():
                violations.append(
                    PolicyViolation(
                        policy_id=self.policy_id,
                        article=self.article,
                        message="Gevoelige gegevens vereisen pseudonimisering",
                        severity=Severity.HIGH,
                        remediation="Pseudonimiseer gegevens waar mogelijk",
                        citation="AVG Art. 32(1)(a)",
                    )
                )

        # Check for access control
        if (
            "toegangscontrole" not in str(measures).lower()
            and "rbac" not in str(measures).lower()
        ):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Toegangscontrole ontbreekt",
                    severity=Severity.HIGH,
                    remediation="Implementeer Role-Based Access Control (RBAC)",
                    citation="AVG Art. 32(2)",
                )
            )

        return PolicyResult(
            policy_id=self.policy_id,
            compliant=len(violations) == 0,
            violations=violations,
            evidence=[f"{len(measures)} beveiligingsmaatregelen geïmplementeerd"]
            if measures
            else [],
        )


# ─── EU AI Act Art. 10: Data Governance ───────────────────────


class AIDataGovernancePolicy(Policy):
    """EU AI Act Art. 10 — Data Governance.

    Training data must be relevant, sufficiently representative,
    and to the best extent possible, free of errors and complete.
    """

    def __init__(self):
        super().__init__(
            policy_id="ai-act-art10-data-governance",
            article="EU AI Act Art. 10(2)(f)",
            description="Data Governance — training data moet relevant en representatief zijn",
        )

    def evaluate(self, context: dict) -> PolicyResult:
        violations = []
        ai_systems = context.get("ai_systems", False)

        if not ai_systems:
            return PolicyResult(policy_id=self.policy_id, compliant=True)

        # Check for bias examination
        if not context.get("bias_examined", False):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Training data is niet onderzocht op mogelijke biases",
                    severity=Severity.HIGH,
                    remediation="Voer bias-auditing uit op training data",
                    citation="EU AI Act Art. 10(3)",
                )
            )

        # Check for data relevance
        if not context.get("data_relevance_documented", False):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Relevantie van training data is niet gedocumenteerd",
                    severity=Severity.MEDIUM,
                    remediation="Documenteer waarom de training data relevant is voor het doel",
                    citation="EU AI Act Art. 10(2)",
                )
            )

        return PolicyResult(
            policy_id=self.policy_id,
            compliant=len(violations) == 0,
            violations=violations,
        )


# ─── EU AI Act Art. 14: Human Oversight ───────────────────────


class HumanOversightPolicy(Policy):
    """EU AI Act Art. 14 — Human Oversight.

    High-risk AI systems must be designed to allow effective oversight.
    """

    def __init__(self):
        super().__init__(
            policy_id="ai-act-art14-human-oversight",
            article="EU AI Act Art. 14",
            description="Human Oversight — hoog-risico AI moet effectieve menselijke tussenkomst mogelijk maken",
        )

    def evaluate(self, context: dict) -> PolicyResult:
        violations = []
        risk_tier = context.get("risk_tier", "minimal")

        if risk_tier != "high":
            return PolicyResult(policy_id=self.policy_id, compliant=True)

        # Check for oversight measures
        if not context.get("oversight_measures"):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Geen menselijke tussenkomstmaatregelen geïmplementeerd",
                    severity=Severity.CRITICAL,
                    remediation="Implementeer Human-in-the-Loop (HITL) of Human-on-the-Loop (HOTL)",
                    citation="EU AI Act Art. 14(1)",
                )
            )

        # Check for stop mechanism
        if not context.get("stop_mechanism"):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Geen stop-kill-switch voor het AI-systeem",
                    severity=Severity.CRITICAL,
                    remediation="Implementeer een kill-switch om het systeem te kunnen stoppen",
                    citation="EU AI Act Art. 14(3)(d)",
                )
            )

        # Check for human override
        if not context.get("human_override"):
            violations.append(
                PolicyViolation(
                    policy_id=self.policy_id,
                    article=self.article,
                    message="Mens kan AI-output niet overrulen",
                    severity=Severity.HIGH,
                    remediation="Implementeer human override capability",
                    citation="EU AI Act Art. 14(3)(c)",
                )
            )

        return PolicyResult(
            policy_id=self.policy_id,
            compliant=len(violations) == 0,
            violations=violations,
        )


# ─── Policy Engine ─────────────────────────────────────────────


class PolicyEngine:
    """Evaluate all compliance policies."""

    def __init__(self):
        self.policies: list[Policy] = [
            DataMinimizationPolicy(),
            SecurityPolicy(),
            AIDataGovernancePolicy(),
            HumanOversightPolicy(),
        ]

    def evaluate_all(self, context: dict) -> list[PolicyResult]:
        """Evaluate all policies against the context."""
        return [policy.evaluate(context) for policy in self.policies]

    def evaluate_policy(self, policy_id: str, context: dict) -> PolicyResult | None:
        """Evaluate a specific policy."""
        for policy in self.policies:
            if policy.policy_id == policy_id:
                return policy.evaluate(context)
        return None

    def get_compliance_summary(self, context: dict) -> dict:
        """Get a compliance summary."""
        results = self.evaluate_all(context)
        total = len(results)
        compliant = sum(1 for r in results if r.compliant)
        violations = [v for r in results for v in r.violations]

        return {
            "total_policies": total,
            "compliant": compliant,
            "non_compliant": total - compliant,
            "compliance_rate": round(compliant / total * 100, 1) if total > 0 else 0,
            "violations": [
                {
                    "policy_id": v.policy_id,
                    "article": v.article,
                    "message": v.message,
                    "severity": v.severity.value,
                    "remediation": v.remediation,
                    "citation": v.citation,
                }
                for v in violations
            ],
            "critical_violations": sum(
                1 for v in violations if v.severity == Severity.CRITICAL
            ),
            "high_violations": sum(
                1 for v in violations if v.severity == Severity.HIGH
            ),
        }
