"""Document Rendering Engine — Fase 4: Tooling & Interoperabiliteit.

Converteert template-dicts naar:
- Markdown (altijd beschikbaar, geen dependencies)
- HTML (met styling voor print/PDF)
- Structured JSON (voor export/integratie)

Optioneel (indien dependencies beschikbaar):
- Word (.docx) via python-docx
- PDF via reportlab of weasyprint

Gebruik:
    from docs.templates.render_engine import render_document
    md = render_document("dpia_pre_scan", "Gemeente Test", format="markdown")
    html = render_document("dpia_pre_scan", "Gemeente Test", format="html")
"""

from __future__ import annotations

import html
from datetime import date
from typing import Any

from . import generate_document


def _flatten_content(content: Any, depth: int = 0) -> list[dict]:
    """Flatten nested dict/liar structure into renderable blocks."""
    blocks: list[dict] = []

    if isinstance(content, dict):
        for key, value in content.items():
            if isinstance(value, str):
                blocks.append(
                    {"type": "text", "content": value, "depth": depth, "key": key}
                )
            elif isinstance(value, dict):
                blocks.append({"type": "section", "title": key, "depth": depth})
                blocks.extend(_flatten_content(value, depth + 1))
            elif isinstance(value, list):
                blocks.append({"type": "list_header", "title": key, "depth": depth})
                for item in value:
                    if isinstance(item, dict):
                        blocks.extend(_flatten_content(item, depth + 1))
                    else:
                        blocks.append(
                            {
                                "type": "list_item",
                                "content": str(item),
                                "depth": depth + 1,
                            }
                        )
            else:
                blocks.append(
                    {"type": "text", "content": str(value), "depth": depth, "key": key}
                )
    elif isinstance(content, str):
        blocks.append({"type": "text", "content": content, "depth": depth})
    elif isinstance(content, list):
        for item in content:
            blocks.extend(_flatten_content(item, depth))

    return blocks


def _render_markdown(doc: dict) -> str:
    """Render document dict to Markdown."""
    lines: list[str] = []

    # Header
    lines.append(f"# {doc.get('document', 'Document')}")
    lines.append("")

    if doc.get("wettelijke_basis"):
        lines.append(f"**Wettelijke basis:** {doc['wettelijke_basis']}")
    if doc.get("organisatie"):
        lines.append(f"**Organisatie:** {doc['organisatie']}")
    if doc.get("datum"):
        lines.append(f"**Datum:** {doc['datum']}")
    if doc.get("model_versie"):
        lines.append(f"**Model versie:** {doc['model_versie']}")
    if doc.get("bron"):
        lines.append(f"**Bron:** {doc['bron']}")

    lines.append("")
    lines.append("---")
    lines.append("")

    # Content
    inhoud = doc.get("inhoud", {})
    blocks = _flatten_content(inhoud)

    for block in blocks:
        btype = block["type"]
        depth = block.get("depth", 0)

        if btype == "section":
            prefix = "#" * min(depth + 2, 6)
            title = block["title"]
            if isinstance(title, str) and title:
                lines.append(f"{prefix} {title}")
                lines.append("")
        elif btype == "text":
            content = block["content"]
            if content and content.strip():
                lines.append(content.strip())
                lines.append("")
        elif btype == "list_header":
            title = block.get("title", "")
            if title:
                lines.append(f"**{title}**")
                lines.append("")
        elif btype == "list_item":
            content = block.get("content", "")
            if content:
                indent = "  " * block.get("depth", 0)
                lines.append(f"{indent}- {content}")

    lines.append("---")
    lines.append(
        f"*Gegenereerd: {date.today().isoformat()} — JuraRegel Document Engine v1.0*"
    )

    return "\n".join(lines)


def _render_html(doc: dict) -> str:
    """Render document dict to HTML (print-ready)."""
    md = _render_markdown(doc)

    # Simple markdown-to-HTML conversion
    html_parts: list[str] = []
    html_parts.append(
        """<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; color: #333; }}
  h1 {{ color: #1a365d; border-bottom: 3px solid #2b6cb0; padding-bottom: 10px; }}
  h2 {{ color: #2c5282; margin-top: 30px; }}
  h3 {{ color: #2d3748; }}
  h4, h5, h6 {{ color: #4a5568; }}
  hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 30px 0; }}
  strong {{ color: #1a365d; }}
  ul, ol {{ padding-left: 20px; }}
  li {{ margin-bottom: 4px; }}
  .meta {{ background: #ebf8ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
  .meta p {{ margin: 4px 0; }}
  footer {{ margin-top: 40px; padding-top: 10px; border-top: 1px solid #e2e8f0; font-size: 0.85em; color: #718096; }}
  @media print {{ body {{ margin: 0; padding: 15px; }} h1 {{ page-break-before: avoid; }} h2 {{ page-break-after: avoid; }} }}
</style>
</head>
<body>""".format(title=html.escape(doc.get("document", "Document")))
    )

    in_list = False
    for line in md.split("\n"):
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_parts.append("</ul>")
                in_list = False
            continue

        if stripped.startswith("# "):
            html_parts.append(f"<h1>{html.escape(stripped[2:])}</h1>")
        elif stripped.startswith("## "):
            html_parts.append(f"<h2>{html.escape(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            html_parts.append(f"<h3>{html.escape(stripped[4:])}</h3>")
        elif stripped.startswith("#### "):
            html_parts.append(f"<h4>{html.escape(stripped[5:])}</h4>")
        elif stripped.startswith("---"):
            html_parts.append("<hr>")
        elif stripped.startswith("- "):
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{html.escape(stripped[2:])}</li>")
        elif stripped.startswith("**") and stripped.endswith("**"):
            html_parts.append(f"<p><strong>{html.escape(stripped[2:-2])}</strong></p>")
        elif (
            stripped.startswith("*")
            and stripped.endswith("*")
            and not stripped.startswith("**")
        ):
            html_parts.append(
                f"<footer><em>{html.escape(stripped[1:-1])}</em></footer>"
            )
        else:
            # Handle inline bold
            text = html.escape(stripped)
            text = text.replace("**", "<strong>", 1)
            while "**" in text:
                text = text.replace("**", "</strong>", 1)
                if "**" in text:
                    text = text.replace("**", "<strong>", 1)
            html_parts.append(f"<p>{text}</p>")

    if in_list:
        html_parts.append("</ul>")

    html_parts.append("</body></html>")
    return "\n".join(html_parts)


def _render_structured(doc: dict) -> dict:
    """Return structured JSON with metadata + flat content blocks."""
    inhoud = doc.get("inhoud", {})
    blocks = _flatten_content(inhoud)

    return {
        "format": "juraregel-structured-v1",
        "generated": date.today().isoformat(),
        "metadata": {
            "document": doc.get("document"),
            "wettelijke_basis": doc.get("wettelijke_basis"),
            "organisatie": doc.get("organisatie"),
            "datum": doc.get("datum"),
            "model_versie": doc.get("model_versie"),
            "bron": doc.get("bron"),
        },
        "content_blocks": blocks,
        "block_count": len(blocks),
    }


def render_document(
    doc_type: str,
    org_naam: str,
    format: str = "markdown",
    **kwargs,
) -> str | dict:
    """Render een document naar het gewenste formaat.

    Args:
        doc_type: Template identifier (bijv. "dpia_pre_scan")
        org_naam: Naam van de organisatie
        format: "markdown", "html", "json", of "structured"
        **kwargs: Extra arguments voor de template

    Returns:
        str (markdown/html) of dict (structured/json)

    Raises:
        ValueError: Onbekend format of onbekend doc_type
    """
    # Default values voor templates die extra args nodig hebben
    defaults = {
        "verwerking": kwargs.get("verwerking", "[verwerking]"),
        "ai_systeem": kwargs.get("ai_systeem", "[AI-systeem]"),
        "systeem": kwargs.get("systeem", "[systeem]"),
        "belang": kwargs.get("belang", "[belang]"),
        "ontvanger_land": kwargs.get("ontvanger_land", "[land]"),
        "ontvanger_naam": kwargs.get("ontvanger_naam", "[ontvanger]"),
    }
    merged = {**defaults, **kwargs}

    doc = generate_document(doc_type, org_naam, **merged)

    if "error" in doc:
        raise ValueError(doc["error"])

    formatters = {
        "markdown": _render_markdown,
        "html": _render_html,
        "json": lambda d: d,  # raw dict
        "structured": _render_structured,
    }

    formatter = formatters.get(format)
    if not formatter:
        raise ValueError(
            f"Onbekend format: {format}. Beschikbaar: {list(formatters.keys())}"
        )

    return formatter(doc)


def render_to_file(
    doc_type: str,
    org_naam: str,
    output_path: str,
    format: str = "markdown",
    **kwargs,
) -> str:
    """Render een document en schrijf naar bestand.

    Returns:
        Absolute path naar het geschreven bestand.
    """
    from pathlib import Path

    result = render_document(doc_type, org_naam, format=format, **kwargs)

    if isinstance(result, dict):
        import json

        result_str = json.dumps(result, indent=2, ensure_ascii=False)
    else:
        result_str = result

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(result_str, encoding="utf-8")

    return str(path.resolve())
