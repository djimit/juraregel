"""Predictive Compliance Engine — Voorspellende compliance-analyse.

Gebaseerd op:
- NIST AI RMF (2023) — Risk-based approach
- Deloitte (2026) — 70% compliance officers naar predictive monitoring
- Stanford Legal Engineering (2025) — Predictive models for regulatory enforcement

Features:
1. Risk Prediction — Welke risico's zijn het meest waarschijnlijk?
2. Trend Analysis — Hoe evolueert de compliance-score?
3. Regulatory Forecast — Aankomende wetswijzigingen
4. Impact Scoring — Welke maatregelen hebben het meeste effect?
5. Early Warning — Alarmsignalen vóórdat problemen optreden
"""

from __future__ import annotations

import json
import logging
import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

# ─── Data Models ──────────────────────────────────────────────


@dataclass
class RiskPrediction:
    """A predicted risk."""

    risk_id: str
    description: str
    probability: float  # 0.0-1.0
    impact: float  # 0.0-1.0
    risk_score: float  # probability * impact
    timeframe: str  # "30d", "90d", "180d"
    recommended_actions: list[str]
    related_frameworks: list[str]


@dataclass
class TrendAnalysis:
    """Compliance score trend."""

    current_score: float
    previous_score: float
    trend: str  # improving, stable, declining
    forecast_30d: float
    forecast_90d: float
    forecast_180d: float
    confidence_interval: tuple[float, float]


@dataclass
class PredictiveReport:
    """Complete predictive compliance report."""

    organisation_id: str
    generated_at: str
    risk_predictions: list[RiskPrediction]
    trend_analysis: TrendAnalysis
    regulatory_forecast: list[dict]
    overall_risk_score: float
    priority_actions: list[str]
    early_warnings: list[str]


# ─── Predictive Engine ────────────────────────────────────────


class PredictiveComplianceEngine:
    """Predict future compliance risks and trends."""

    # Risk factors and their base probabilities
    RISK_FACTORS = {
        "datalek": {
            "base_probability": 0.15,
            "frameworks": ["AVG"],
            "triggers": ["gevoelige gegevens", "grootschalig", "geen encryptie"],
        },
        "discriminatie": {
            "base_probability": 0.10,
            "frameworks": ["AVG", "AI Act"],
            "triggers": ["ai_systems", "profiling", "etniciteit"],
        },
        "non_conformiteit_ai_act": {
            "base_probability": 0.20,
            "frameworks": ["AI Act"],
            "triggers": ["ai_systems", "hoog_risico", "geen_fria"],
        },
        "dpia_vergeten": {
            "base_probability": 0.25,
            "frameworks": ["AVG"],
            "triggers": ["hoog_risico", "geen_dpia", "nieuwe_verwerking"],
        },
        "evidence_verlopen": {
            "base_probability": 0.30,
            "frameworks": ["AVG", "AI Act"],
            "triggers": ["verouderde_bewijsstukken", "geen_review"],
        },
        "toegang_onvoldoende": {
            "base_probability": 0.18,
            "frameworks": ["AVG", "ISO 27001"],
            "triggers": ["geen_rbac", "te_veel_toegang", "geen_mfa"],
        },
    }

    def predict(self, organisation_id: str, current_state: dict) -> PredictiveReport:
        """Generate a predictive compliance report."""
        start = time.time()

        # 1. Risk predictions
        risk_predictions = self._predict_risks(current_state)

        # 2. Trend analysis
        trend = self._analyze_trend(current_state)

        # 3. Regulatory forecast
        regulatory_forecast = self._forecast_regulatory_changes(current_state)

        # 4. Overall risk score
        overall_risk = sum(r.risk_score for r in risk_predictions) / max(
            len(risk_predictions), 1
        )

        # 5. Priority actions
        priority_actions = self._generate_priority_actions(risk_predictions)

        # 6. Early warnings
        early_warnings = self._generate_early_warnings(risk_predictions, current_state)

        return PredictiveReport(
            organisation_id=organisation_id,
            generated_at=datetime.utcnow().isoformat(),
            risk_predictions=risk_predictions,
            trend_analysis=trend,
            regulatory_forecast=regulatory_forecast,
            overall_risk_score=round(overall_risk, 3),
            priority_actions=priority_actions,
            early_warnings=early_warnings,
        )

    def _predict_risks(self, state: dict) -> list[RiskPrediction]:
        """Predict risks based on current state."""
        predictions = []

        for risk_id, factor in self.RISK_FACTORS.items():
            # Calculate probability based on triggers
            probability = factor["base_probability"]
            triggers_met = 0

            for trigger in factor["triggers"]:
                if self._check_trigger(trigger, state):
                    triggers_met += 1
                    probability += 0.10  # +10% per trigger

            probability = min(probability, 0.95)

            # Calculate impact
            impact = self._calculate_impact(risk_id, state)

            # Determine timeframe
            if probability > 0.5:
                timeframe = "30d"
            elif probability > 0.3:
                timeframe = "90d"
            else:
                timeframe = "180d"

            predictions.append(
                RiskPrediction(
                    risk_id=risk_id,
                    description=self._get_risk_description(risk_id),
                    probability=round(probability, 3),
                    impact=round(impact, 3),
                    risk_score=round(probability * impact, 3),
                    timeframe=timeframe,
                    recommended_actions=self._get_risk_actions(risk_id),
                    related_frameworks=factor["frameworks"],
                )
            )

        # Sort by risk score
        predictions.sort(key=lambda r: r.risk_score, reverse=True)
        return predictions

    def _check_trigger(self, trigger: str, state: dict) -> bool:
        """Check if a risk trigger is present."""
        trigger_lower = trigger.lower()
        state_str = json.dumps(state).lower()
        return trigger_lower in state_str

    def _calculate_impact(self, risk_id: str, state: dict) -> float:
        """Calculate impact of a risk."""
        impact_scores = {
            "datalek": 0.9,
            "discriminatie": 0.8,
            "non_conformiteit_ai_act": 0.7,
            "dpia_vergeten": 0.6,
            "evidence_verlopen": 0.4,
            "toegang_onvoldoende": 0.7,
        }
        return impact_scores.get(risk_id, 0.5)

    def _get_risk_description(self, risk_id: str) -> str:
        """Get human-readable risk description."""
        descriptions = {
            "datalek": "Risico op datalek door onvoldoende beveiliging",
            "discriminatie": "Risico op discriminatie door AI-systeem",
            "non_conformiteit_ai_act": "Non-conformiteit met EU AI Act verplichtingen",
            "dpia_vergeten": "DPIA niet uitgevoerd waar verplicht",
            "evidence_verlopen": "Bewijsstukken verlopen of verouderd",
            "toegang_onvoldoende": "Onvoldoende toegangscontrole",
        }
        return descriptions.get(risk_id, f"Risico: {risk_id}")

    def _get_risk_actions(self, risk_id: str) -> list[str]:
        """Get recommended actions for a risk."""
        actions = {
            "datalek": [
                "Implementeer encryptie",
                "Voer penetratietest uit",
                "Update incident response plan",
            ],
            "discriminatie": [
                "Voer bias-audit uit",
                "Documenteer fairness-metrics",
                "Implementeer human oversight",
            ],
            "non_conformiteit_ai_act": [
                "Voer FRIA uit",
                "Stel technische documentatie op",
                "Implementeer risicobeheer",
            ],
            "dpia_vergeten": [
                "Voer DPIA uit",
                "Documenteer verwerkingsdoelen",
                "Identificeer maatregelen",
            ],
            "evidence_verlopen": [
                "Vernieuw bewijsstukken",
                "Plan review in",
                "Documenteer actualiteit",
            ],
            "toegang_onvoldoende": [
                "Implementeer RBAC",
                "Activeer MFA",
                "Review toegangsrechten",
            ],
        }
        return actions.get(risk_id, ["Analyseer risico", "Neem maatregelen"])

    def _analyze_trend(self, state: dict) -> TrendAnalysis:
        """Analyze compliance score trend."""
        current_score = state.get("compliance_score", 50) or 50
        previous_score = state.get("previous_compliance_score") or current_score

        # Simple trend extrapolation
        delta = current_score - previous_score
        if delta > 5:
            trend = "improving"
        elif delta < -5:
            trend = "declining"
        else:
            trend = "stable"

        # Forecast with decay
        forecast_30d = current_score + delta * 0.5
        forecast_90d = current_score + delta * 0.3
        forecast_180d = current_score + delta * 0.1

        # Confidence interval (wider for longer horizon)
        ci_30 = (forecast_30d - 5, forecast_30d + 5)
        ci_90 = (forecast_90d - 10, forecast_90d + 10)

        return TrendAnalysis(
            current_score=current_score,
            previous_score=previous_score,
            trend=trend,
            forecast_30d=round(max(0, min(100, forecast_30d)), 1),
            forecast_90d=round(max(0, min(100, forecast_90d)), 1),
            forecast_180d=round(max(0, min(100, forecast_180d)), 1),
            confidence_interval=ci_30,
        )

    def _forecast_regulatory_changes(self, state: dict) -> list[dict]:
        """Forecast upcoming regulatory changes."""
        # Based on known upcoming deadlines
        now = datetime.utcnow()
        forecasts = [
            {
                "change": "EU AI Act — Hoog-risico systemen volledig van kracht",
                "deadline": "2026-08-02",
                "days_remaining": (datetime(2026, 8, 2) - now).days,
                "impact": "critical" if state.get("ai_systems") else "low",
                "action_required": "Alle hoog-risico AI-systemen moeten conform zijn",
            },
            {
                "change": "EDPB — Nieuwe richtlijnen AI en data protection",
                "deadline": "2026-12-01",
                "days_remaining": (datetime(2026, 12, 1) - now).days,
                "impact": "medium",
                "action_required": "Review DPIA's op nieuwe criteria",
            },
        ]
        return forecasts

    def _generate_priority_actions(
        self, predictions: list[RiskPrediction]
    ) -> list[str]:
        """Generate priority actions."""
        actions = []
        for pred in predictions[:3]:  # Top 3 risks
            actions.extend(pred.recommended_actions[:2])
        return list(dict.fromkeys(actions))  # Deduplicate

    def _generate_early_warnings(
        self, predictions: list[RiskPrediction], state: dict
    ) -> list[str]:
        """Generate early warnings."""
        warnings = []
        for pred in predictions:
            if pred.probability > 0.5:
                warnings.append(
                    f"HOOG RISICO: {pred.description} (kans: {pred.probability * 100:.0f}%)"
                )
            elif pred.probability > 0.3:
                warnings.append(
                    f"MEDIUM RISICO: {pred.description} (kans: {pred.probability * 100:.0f}%)"
                )
        return warnings


# ─── Singleton ─────────────────────────────────────────────────

predictive_engine = PredictiveComplianceEngine()
