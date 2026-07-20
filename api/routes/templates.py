"""Template Service API — CRUD + generate + validate + render."""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Any

router = APIRouter()


# ─── Request/Response Models ──────────────────────────────────


class GenerateRequest(BaseModel):
    """Request to generate a document from a template."""

    organisation: str = Field(..., min_length=1, description="Naam van de organisatie")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Template parameters"
    )


class RenderRequest(BaseModel):
    """Request to render a document to a specific format."""

    organisation: str = Field(..., min_length=1)
    parameters: dict[str, Any] = Field(default_factory=dict)
    format: str = Field(
        default="markdown", description="markdown, html, json, structured"
    )


class TemplateInfo(BaseModel):
    """Template metadata."""

    id: str
    document: str
    wettelijke_basis: str
    model_versie: str
    section_count: int
    has_checkboxes: bool
    has_scoring: bool
    category: str


# ─── Endpoints ────────────────────────────────────────────────


@router.get("/", response_model=list[TemplateInfo])
async def list_templates(
    category: str | None = Query(None, description="Filter op categorie"),
    has_checkboxes: bool | None = Query(
        None, description="Filter op interactieve templates"
    ),
):
    """List all available templates with metadata."""
    from docs.templates import list_documents, generate_document, enrich_document
    from docs.templates.template_schema import get_template_info

    documents = list_documents()
    results = []

    for doc_info in documents:
        doc_id = doc_info["id"]
        try:
            doc = generate_document(doc_id, "Example")
            enriched = enrich_document(doc)
            info = get_template_info(enriched)

            if category and info.get("category") != category:
                continue
            if has_checkboxes is not None and info["has_checkboxes"] != has_checkboxes:
                continue

            results.append(
                TemplateInfo(
                    id=doc_id,
                    document=enriched.get("document", doc_id),
                    wettelijke_basis=enriched.get("wettelijke_basis", ""),
                    model_versie=enriched.get("model_versie", ""),
                    section_count=info["section_count"],
                    has_checkboxes=info["has_checkboxes"],
                    has_scoring=info["has_scoring"],
                    category=info.get("category", "Overig"),
                )
            )
        except Exception:
            pass

    return results


@router.get("/{template_id}")
async def get_template(template_id: str):
    """Get template metadata and structure."""
    from docs.templates import generate_document, enrich_document, list_documents
    from docs.templates.template_schema import (
        get_template_info,
        list_template_capabilities,
    )

    valid_ids = {d["id"] for d in list_documents()}
    if template_id not in valid_ids:
        raise HTTPException(
            status_code=404, detail=f"Template not found: {template_id}"
        )

    try:
        doc = generate_document(template_id, "Example")
        enriched = enrich_document(doc)
        info = get_template_info(enriched)
        capabilities = list_template_capabilities(enriched)

        return {
            "id": template_id,
            **info,
            "capabilities": capabilities,
            "structure": list(enriched.get("inhoud", {}).keys()),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{template_id}/generate")
async def generate_document_endpoint(template_id: str, request: GenerateRequest):
    """Generate a document from a template."""
    from docs.templates import generate_document, enrich_document, validate_document

    doc = generate_document(template_id, request.organisation, **request.parameters)
    if "error" in doc:
        raise HTTPException(status_code=404, detail=doc["error"])

    enriched = enrich_document(doc)
    validate_document(enriched)

    return {
        "template_id": template_id,
        "document": enriched,
    }


@router.post("/{template_id}/render")
async def render_document_endpoint(template_id: str, request: RenderRequest):
    """Render a document to a specific format."""
    from docs.templates.render_engine import render_document

    try:
        result = render_document(
            template_id,
            request.organisation,
            format=request.format,
            **request.parameters,
        )
        return {
            "template_id": template_id,
            "format": request.format,
            "content": result,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{template_id}/validate")
async def validate_document_endpoint(template_id: str, request: GenerateRequest):
    """Validate a document against the template schema."""
    from docs.templates import generate_document, enrich_document, validate_document
    from docs.templates.template_schema import get_template_info

    doc = generate_document(template_id, request.organisation, **request.parameters)
    if "error" in doc:
        raise HTTPException(status_code=404, detail=doc["error"])

    enriched = enrich_document(doc)

    try:
        validate_document(enriched)
        info = get_template_info(enriched)
        return {
            "valid": True,
            "template_id": template_id,
            "section_count": info["section_count"],
            "has_checkboxes": info["has_checkboxes"],
            "has_scoring": info["has_scoring"],
        }
    except Exception as e:
        return {
            "valid": False,
            "template_id": template_id,
            "error": str(e),
        }
