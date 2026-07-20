"""JuraRegel API — FastAPI application entry point.

Living Compliance Engine REST API.
Provides endpoints for templates, assessments, processing activities,
evidence linking, regulatory monitoring, and compliance scoring.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import close_database, init_database
from .routes import (
    templates,
    assessments,
    processing,
    evidence,
    health,
    agents,
    compliance,
    policies,
    rag,
    drift,
    regulatory,
    knowledge_graph,
    benchmarks,
    ci,
    reasoning,
    predictive,
    learning,
    accountability,
    jurisdiction,
    digital_twin,
    orchestrator,
    reports,
    evaluation,
)
from .middleware import RateLimitMiddleware, TenantMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup + shutdown."""
    # Startup
    # await init_database()  # Uncomment when PostgreSQL is available
    yield
    # Shutdown
    # await close_database()


app = FastAPI(
    title="JuraRegel Compliance API",
    description="""
    ## Living Compliance Engine v4.0

    API voor continue compliance-monitoring, assessment-generatie,
    juridische regel-traceability, en AI-gestuurde analyse.

    ### Authenticatie
    Alle endpoints (behalve `/health`) vereisen een Bearer token.

    ### Multi-tenancy
    Elke request bevat een `X-Tenant-ID` header met de organisatie-ID.
    Data-isolation wordt afgedwongen op database-niveau (RLS).

    ### AI Agents
    `/api/v1/agents/` biedt toegang tot autonome compliance-agents:
    - DPIA Agent — End-to-end DPIA generatie
    - FRIA Agent — End-to-end FRIA generatie
    - Regulatory Monitor — Continue wetswijzigingsdetectie
    """,
    version="4.0.0",
    contact={
        "name": "JuraRegel",
        "url": "https://github.com/djimit/juraregel",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
app.add_middleware(TenantMiddleware)

# Routes
app.include_router(health.router, tags=["System"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["Templates"])
app.include_router(
    assessments.router, prefix="/api/v1/assessments", tags=["Assessments"]
)
app.include_router(
    processing.router,
    prefix="/api/v1/processing-activities",
    tags=["Processing Activities"],
)
app.include_router(evidence.router, prefix="/api/v1/evidence", tags=["Evidence"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["AI Agents"])
app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["Compliance"])
app.include_router(policies.router, prefix="/api/v1/policies", tags=["Policies"])
app.include_router(rag.router, prefix="/api/v1/rag", tags=["RAG"])
app.include_router(drift.router, prefix="/api/v1/drift", tags=["Drift Detection"])
app.include_router(
    regulatory.router, prefix="/api/v1/regulatory", tags=["Regulatory Monitor"]
)
app.include_router(
    knowledge_graph.router, prefix="/api/v1/knowledge-graph", tags=["Knowledge Graph"]
)
app.include_router(benchmarks.router, prefix="/api/v1/benchmarks", tags=["Benchmarks"])
app.include_router(ci.router, prefix="/api/v1/ci", tags=["CI Gates"])
app.include_router(
    reasoning.router, prefix="/api/v1/reasoning", tags=["Legal Reasoning"]
)
app.include_router(
    predictive.router, prefix="/api/v1/predictive", tags=["Predictive Compliance"]
)
app.include_router(learning.router, prefix="/api/v1/learning", tags=["Self-Learning"])
app.include_router(
    accountability.router, prefix="/api/v1/accountability", tags=["Accountable AI"]
)
app.include_router(
    jurisdiction.router, prefix="/api/v1/jurisdiction", tags=["Multi-Jurisdiction"]
)
app.include_router(
    digital_twin.router, prefix="/api/v1/digital-twin", tags=["Digital Twin"]
)
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(evaluation.router, prefix="/api/v1/evaluation", tags=["Evaluation"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])


@app.get("/", tags=["Root"])
async def root():
    """API root — returns service info."""
    return {
        "service": "JuraRegel Compliance API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "endpoints": {
            "templates": "/api/v1/templates",
            "assessments": "/api/v1/assessments",
            "processing_activities": "/api/v1/processing-activities",
            "evidence": "/api/v1/evidence",
        },
    }
