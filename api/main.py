"""JuraRegel API — FastAPI application entry point.

Living Compliance Engine REST API.
Provides endpoints for templates, assessments, processing activities,
evidence linking, regulatory monitoring, and compliance scoring.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import templates, assessments, processing, evidence, health
from .middleware import RateLimitMiddleware, TenantMiddleware

app = FastAPI(
    title="JuraRegel Compliance API",
    description="""
    ## Living Compliance Engine

    API voor continue compliance-monitoring, assessment-generatie,
    en juridische regel-traceability.

    ### Authenticatie
    Alle endpoints (behalve `/health`) vereisen een Bearer token.
    Gebruik `/auth/token` om een token te verkrijgen.

    ### Multi-tenancy
    Elke request bevat een `X-Tenant-Header` met de organisatie-ID.
    Data-isolation wordt afgedwongen op database-niveau (RLS).
    """,
    version="1.0.0",
    contact={
        "name": "JuraRegel",
        "url": "https://github.com/djimit/juraregel",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
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
