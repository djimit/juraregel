"""AI Agents API — Autonomous compliance agents."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


# ─── Request Models ──────────────────────────────────────────


class AgentRequest(BaseModel):
    """Request to run an agent."""

    organisation_id: str = Field(..., description="ID van de organisatie")
    parameters: dict[str, Any] = Field(default_factory=dict)


class DPIARequest(BaseModel):
    """Request to run the DPIA agent."""

    organisation_id: str
    processing_activity: dict[str, Any]


class FRIARequest(BaseModel):
    """Request to run the FRIA agent."""

    organisation_id: str
    ai_system: dict[str, Any]


# ─── Endpoints ────────────────────────────────────────────────


@router.get("/")
async def list_agents():
    """List available agents."""
    return {
        "agents": [
            {
                "id": "dpia",
                "name": "DPIA Agent",
                "description": "End-to-end DPIA generatie met pre-scan, risico-analyse, en maatregelen",
                "version": "1.0.0",
                "status": "active",
            },
            {
                "id": "fria",
                "name": "FRIA Agent",
                "description": "End-to-end FRIA generatie met risicoclassificatie en grondrechten-analyse",
                "version": "1.0.0",
                "status": "active",
            },
            {
                "id": "regulatory",
                "name": "Regulatory Monitor",
                "description": "Continue wetswijzigingsdetectie met impact-analyse",
                "version": "1.0.0",
                "status": "active",
            },
        ]
    }


@router.post("/dpia/run")
async def run_dpia_agent(request: DPIARequest):
    """Run the DPIA agent for a processing activity."""
    from ..agents import DPIAAgent

    agent = DPIAAgent()
    result = await agent.execute(request.processing_activity)

    return {
        "agent": result.agent,
        "status": result.status,
        "output": result.output,
        "citations": result.citations,
        "confidence": result.confidence,
        "recommendations": result.recommendations,
        "execution_time_ms": result.execution_time_ms,
        "trace": result.trace,
    }


@router.post("/fria/run")
async def run_fria_agent(request: FRIARequest):
    """Run the FRIA agent for an AI system."""
    from ..agents import FRIAAgent

    agent = FRIAAgent()
    result = await agent.execute(request.ai_system)

    return {
        "agent": result.agent,
        "status": result.status,
        "output": result.output,
        "citations": result.citations,
        "confidence": result.confidence,
        "recommendations": result.recommendations,
        "execution_time_ms": result.execution_time_ms,
        "trace": result.trace,
    }


@router.post("/regulatory/scan")
async def run_regulatory_scan():
    """Run the regulatory monitor agent."""
    from ..agents import RegulatoryMonitorAgent

    agent = RegulatoryMonitorAgent()
    result = await agent.scan()

    return {
        "agent": result.agent,
        "status": result.status,
        "output": result.output,
        "confidence": result.confidence,
        "execution_time_ms": result.execution_time_ms,
    }


@router.post("/full-check")
async def run_full_compliance_check(request: AgentRequest):
    """Run a full compliance check across all agents."""
    from ..agents import AgentOrchestrator

    orchestrator = AgentOrchestrator()
    results = await orchestrator.run_full_compliance_check(request.organisation_id)

    return results
