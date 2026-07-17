# NIST AI RMF → NEDERUS Crosswalk

Maps NIST AI Risk Management Framework 1.0 Core Functions to NEDERUS unified controls.

## GOVERN

| NIST Subfunction | NEDERUS Control | Relation |
|-----------------|-----------------|----------|
| GOVERN-1.1: Organizational accountability | NED-03 (Human Oversight) | partial |
| GOVERN-1.2: Policies and procedures | NED-01 (AI Impact Assessment) | partial |
| GOVERN-1.3: Risk management integration | NED-01 (AI Impact Assessment) | equivalent |
| GOVERN-1.4: Human oversight policies | NED-03 (Human Oversight) | equivalent |
| GOVERN-1.5: Training and awareness | — | gap (organizational, not per-system) |
| GOVERN-1.6: Stakeholder engagement | NED-01 (AI Impact Assessment) | partial |

## MAP

| NIST Subfunction | NEDERUS Control | Relation |
|-----------------|-----------------|----------|
| MAP-1.1: Identify and assess risks | NED-01 (AI Impact Assessment) | equivalent |
| MAP-1.2: Context and scope | NED-01 (AI Impact Assessment) | equivalent |
| MAP-2.1: Categorize AI system | NED-01 (AI Impact Assessment) | partial |
| MAP-2.2: Assess impacts | NED-01 (AI Impact Assessment) | equivalent |
| MAP-2.3: Potential impacts to individuals | NED-02 (Bias & Fairness) | equivalent |
| MAP-3.1: Prioritize risks | NED-01 (AI Impact Assessment) | partial |
| MAP-4.1: Risk treatment decisions | NED-01 (AI Impact Assessment) | partial |

## MEASURE

| NIST Subfunction | NEDERUS Control | Relation |
|-----------------|-----------------|----------|
| MEASURE-1.1: Metrics selection | NED-02 (Bias & Fairness) | partial |
| MEASURE-1.2: AI system trustworthiness | NED-02 (Bias & Fairness) | equivalent |
| MEASURE-1.3: Explainability and interpretability | NED-04 (Transparency) | equivalent |
| MEASURE-2.1: Monitor and evaluate | NED-02 (Bias & Fairness) | partial |
| MEASURE-3.1: Feedback and improvement | NED-05 (Incident Response) | partial |

## MANAGE

| NIST Subfunction | NEDERUS Control | Relation |
|-----------------|-----------------|----------|
| MANAGE-1.1: Risk treatment | NED-01 (AI Impact Assessment) | partial |
| MANAGE-2.1: Human intervention | NED-03 (Human Oversight) | equivalent |
| MANAGE-2.2: System changes | — | gap (covered by BIO2 change management) |
| MANAGE-2.3: Incident response and recovery | NED-05 (Incident Response) | equivalent |
| MANAGE-3.1: Post-deployment monitoring | NED-02 (Bias & Fairness) | partial |

## Coverage Summary

- **GOVERN**: 5/6 subfunctions mapped (83%)
- **MAP**: 7/7 subfunctions mapped (100%)
- **MEASURE**: 5/5 subfunctions mapped (100%)
- **MANAGE**: 4/5 subfunctions mapped (80%)

**Overall NIST AI RMF coverage: 21/23 subfunctions (91%)**

Unmapped subfunctions:
- GOVERN-1.5: Training and awareness (organizational, not per-AI-system)
- MANAGE-2.2: System changes (covered by BIO2 change management controls)
