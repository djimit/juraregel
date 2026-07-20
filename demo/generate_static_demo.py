#!/usr/bin/env python3
"""Generate the JuraRegel product demo for GitHub Pages.

Produces a self-contained single-page application showcasing:
- Hero + product positioning
- Interactive compliance calculator
- Architecture visualization
- Template browser (37 templates)
- 4-phase methodology
- API documentation preview
- Evidence linking demo

Usage:
    python demo/generate_static_demo.py
    # Output: demo/index.html
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docs.templates import generate_document, enrich_document, list_documents
from docs.templates.render_engine import render_document
from docs.templates.template_schema import get_template_info


# ─── Template metadata ────────────────────────────────────────

CATEGORIES = {
    "Privacy": [
        "dpia",
        "privacyverklaring",
        "verwerkersovereenkomst",
        "rova",
        "datalek_procedure",
        "toestemmingsregister",
    ],
    "Informatiebeveiliging": [
        "ib_beleid",
        "statement_of_applicability",
        "risicoanalyse",
        "bcp",
        "incident_response",
    ],
    "AI & Algoritmes": [
        "fria",
        "algoritmeregister",
        "technische_documentatie_ai",
        "dpia_rijksdienst",
        "iama",
        "fria_eu",
    ],
    "Kwaliteit & Compliance": [
        "nis2_cybersecurity",
        "kwaliteitsbeleid",
        "milieubeleid",
        "arbobeleid",
        "zorg_ib_beleid",
    ],
    "Fase 1 — Wettelijk Kritiek": [
        "dpia_pre_scan",
        "lia",
        "tia",
        "ai_risicoclassificatie",
        "privacy_by_design",
    ],
    "Fase 2 — Methodologisch": [
        "dpia_fria_overlap",
        "risico_methodiek",
        "bias_audit",
        "human_oversight",
        "bewaarbeleid",
    ],
    "Fase 3 — Academisch Diep": [
        "ethics_by_design",
        "value_sensitive_design",
        "nist_ai_rmf",
        "stakeholder_consultatie",
        "dpia_review",
    ],
}

PHASES = [
    {
        "id": "phase-1",
        "title": "Registreren",
        "icon": "📋",
        "description": "Verwerkingsactiviteiten registreren in het verwerkingsregister (AVG Art. 30). Automatische detectie van DPIA/FRIA-verplichtingen.",
        "color": "#3182ce",
    },
    {
        "id": "phase-2",
        "title": "Beoordelen",
        "icon": "⚖️",
        "description": "Risico-analyse met 37 evidence-based templates. RAG-gestuurde juridische analyse met bron-citaties.",
        "color": "#38a169",
    },
    {
        "id": "phase-3",
        "title": "Mitigeren",
        "icon": "🛡️",
        "description": "Geprioriteerde maatregelen met juridische basis. Workflow-gestuurde implementatie met verantwoordelijkheden.",
        "color": "#d69e2e",
    },
    {
        "id": "phase-4",
        "title": "Monitoren",
        "icon": "📊",
        "description": "Continue compliance-monitoring, wetswijzigingsdetectie, en real-time compliance scoring.",
        "color": "#805ad5",
    },
]


def get_category(doc_id: str) -> str:
    for cat, ids in CATEGORIES.items():
        if doc_id in ids:
            return cat
    return "Overig"


def generate_demo():
    """Generate the full product demo HTML."""
    documents = list_documents()

    templates_data = []
    for doc_info in documents:
        doc_id = doc_info["id"]
        try:
            doc = generate_document(doc_id, "Organisatie Voorbeeld")
            enriched = enrich_document(doc)
            info = get_template_info(enriched)
            md = render_document(doc_id, "Organisatie Voorbeeld", format="markdown")

            templates_data.append(
                {
                    "id": doc_id,
                    "category": get_category(doc_id),
                    "document": enriched.get("document", doc_id),
                    "wettelijke_basis": enriched.get("wettelijke_basis", ""),
                    "model_versie": enriched.get("model_versie", ""),
                    "section_count": info["section_count"],
                    "has_checkboxes": info["has_checkboxes"],
                    "has_scoring": info["has_scoring"],
                    "markdown": md[:500],
                }
            )
        except Exception as e:
            print(f"  Warning: {doc_id} skipped: {e}")

    html = _build_html(templates_data)

    output_path = ROOT / "demo" / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated demo: {output_path}")
    print(f"Templates: {len(templates_data)}")
    print(f"File size: {len(html):,} bytes")


def _build_html(templates: list[dict]) -> str:
    templates_json = json.dumps(templates, ensure_ascii=False)
    phases_json = json.dumps(PHASES, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JuraRegel — Living Compliance Engine</title>
<meta name="description" content="JuraRegel: 37 compliance templates, AI-gestuurde juridische analyse, continue monitoring. Van DPIA tot FRIA, van wetgeving tot implementatie.">
<style>
:root {{
  --primary: #1a365d;
  --primary-light: #2b6cb0;
  --accent: #38a169;
  --accent-light: #68d391;
  --bg: #f7fafc;
  --card-bg: #ffffff;
  --text: #2d3748;
  --text-light: #718096;
  --border: #e2e8f0;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 40px rgba(0,0,0,0.15);
  --radius: 12px;
  --radius-sm: 8px;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height:: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}

/* ─── Navigation ──────────────────────────────────────────── */
.nav {{ background: var(--card-bg); border-bottom: 1px solid var(--border); padding: 16px 0; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(10px); background: rgba(255,255,255,0.95); }}
.nav-inner {{ display: flex; align-items: center; justify-content: space-between; max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
.nav-logo {{ font-size: 1.3rem; font-weight: 700; color: var(--primary); text-decoration: none; }}
.nav-links {{ display: flex; gap: 24px; }}
.nav-links a {{ color: var(--text); text-decoration: none; font-size: 0.9rem; font-weight: 500; transition: color 0.2s; }}
.nav-links a:hover {{ color: var(--primary-light); }}

/* ─── Hero ────────────────────────────────────────────────── */
.hero {{ background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%); color: white; padding: 80px 20px; text-align: center; }}
.hero h1 {{ font-size: 2.8rem; font-weight: 800; margin-bottom: 16px; letter-spacing: -0.02em; }}
.hero p {{ font-size: 1.2rem; opacity: 0.9; max-width: 700px; margin: 0 auto 32px; }}
.hero-stats {{ display: flex; gap: 40px; justify-content: center; flex-wrap: wrap; margin-top: 40px; }}
.stat {{ text-align: center; }}
.stat-value {{ font-size: 2rem; font-weight: 700; }}
.stat-label {{ font-size: 0.85rem; opacity: 0.8; }}
.hero-badges {{ display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 24px; }}
.badge {{ background: rgba(255,255,255,0.15); padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; backdrop-filter: blur(5px); }}

/* ─── Sections ───────────────────────────────────────────── */
.section {{ padding: 60px 0; }}
.section-title {{ font-size: 1.8rem; font-weight: 700; color: var(--primary); margin-bottom: 8px; text-align: center; }}
.section-subtitle {{ color: var(--text-light); text-align: center; margin-bottom: 40px; font-size: 1rem; }}

/* ─── Phases ─────────────────────────────────────────────── */
.phases-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }}
.phase-card {{ background: var(--card-bg); border-radius: var(--radius); padding: 28px; box-shadow: var(--shadow); border-top: 4px solid var(--phase-color, var(--primary)); transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; }}
.phase-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-lg); }}
.phase-icon {{ font-size: 2rem; margin-bottom: 12px; }}
.phase-title {{ font-size: 1.15rem; font-weight: 600; margin-bottom: 8px; color: var(--primary); }}
.phase-desc {{ font-size: 0.9rem; color: var(--text-light); line-height: 1.5; }}

/* ─── Calculator ─────────────────────────────────────────── */
.calculator {{ background: var(--card-bg); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); max-width: 600px; margin: 0 auto; }}
.calc-group {{ margin-bottom: 20px; }}
.calc-label {{ display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }}
.calc-select {{ width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 0.9rem; background: white; }}
.calc-select:focus {{ outline: none; border-color: var(--primary-light); }}
.calc-result {{ background: #ebf8ff; border-radius: var(--radius-sm); padding: 20px; margin-top: 24px; text-align: center; }}
.calc-score {{ font-size: 3rem; font-weight: 800; color: var(--primary); }}
.calc-label-score {{ font-size: 0.9rem; color: var(--text-light); margin-top: 4px; }}
.calc-verdict {{ margin-top: 12px; padding: 8px 16px; border-radius: 20px; font-weight: 600; display: inline-block; }}

/* ─── Templates ──────────────────────────────────────────── */
.controls {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; align-items: center; }}
.search {{ flex: 1; min-width: 200px; padding: 10px 16px; border: 1px solid var(--border); border-radius: var(--radius-sm); font-size: 0.9rem; }}
.search:focus {{ outline: none; border-color: var(--primary-light); }}
.filter-btns {{ display: flex; gap: 8px; flex-wrap: wrap; }}
.filter-btn {{ padding: 8px 14px; border: 1px solid var(--border); background: var(--card-bg); border-radius: var(--radius-sm); cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }}
.filter-btn:hover {{ border-color: var(--primary-light); }}
.filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}

.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }}
.card {{ background: var(--card-bg); border-radius: var(--radius-sm); padding: 20px; box-shadow: var(--shadow); cursor: pointer; transition: all 0.2s; border: 2px solid transparent; }}
.card:hover {{ border-color: var(--primary-light); transform: translateY(-2px); box-shadow: var(--shadow-lg); }}
.card-category {{ font-size: 0.7rem; color: var(--primary-light); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
.card-title {{ font-size: 1rem; font-weight: 600; margin-bottom: 6px; color: var(--primary); }}
.card-meta {{ font-size: 0.8rem; color: var(--text-light); margin-bottom: 8px; }}
.card-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.tag {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; background: #ebf8ff; color: var(--primary-light); }}
.tag.scoring {{ background: #f0fff4; color: var(--accent); }}

/* ─── Architecture ───────────────────────────────────────── */
.arch-diagram {{ background: var(--card-bg); border-radius: var(--radius); padding: 32px; box-shadow: var(--shadow); overflow-x: auto; }}
.arch-layer {{ display: flex; gap: 12px; margin-bottom: 16px; align-items: stretch; }}
.arch-layer:last-child {{ margin-bottom: 0; }}
.arch-label {{ min-width: 120px; font-weight: 600; font-size: 0.85rem; color: var(--primary); display: flex; align-items: center; }}
.arch-boxes {{ display: flex; gap: 8px; flex-wrap: wrap; flex: 1; }}
.arch-box {{ background: #ebf8ff; border: 1px solid #bee3f8; border-radius: var(--radius-sm); padding: 10px 14px; font-size: 0.8rem; font-weight: 500; text-align: center; flex: 1; min-width: 100px; }}
.arch-box.ai {{ background: #f0fff4; border-color: #c6f6d5; }}
.arch-box.data {{ background: #faf5ff; border-color: #e9d8fd; }}
.arch-box.core {{ background: #fffff0; border-color: #fefcbf; }}

/* ─── Modal ──────────────────────────────────────────────── */
.modal-overlay {{ display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); z-index: 1000; overflow-y: auto; }}
.modal-overlay.active {{ display: flex; justify-content: center; padding: 40px 20px; }}
.modal {{ background: var(--card-bg); border-radius: var(--radius); max-width: 800px; width: 100%; max-height: 85vh; overflow-y: auto; box-shadow: var(--shadow-lg); }}
.modal-header {{ padding: 24px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: var(--card-bg); z-index: 10; }}
.modal-header h2 {{ font-size: 1.3rem; color: var(--primary); }}
.modal-header .meta {{ font-size: 0.85rem; color: var(--text-light); margin-top: 4px; }}
.modal-close {{ position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-light); }}
.modal-close:hover {{ color: var(--text); }}
.modal-body {{ padding: 24px; }}
.modal-body h3 {{ font-size: 1.1rem; color: var(--primary); margin: 20px 0 10px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }}
.modal-body h4 {{ font-size: 1rem; color: var(--text); margin: 16px 0 8px; }}
.modal-body p {{ margin-bottom: 10px; }}
.modal-body ul, .modal-body ol {{ padding-left: 20px; margin-bottom: 10px; }}
.modal-body li {{ margin-bottom: 4px; }}
.modal-body strong {{ color: var(--primary); }}
.modal-body hr {{ border: none; border-top: 1px solid var(--border); margin: 20px 0; }}
.modal-body em {{ color: var(--text-light); }}

/* ─── Footer ─────────────────────────────────────────────── */
.footer {{ background: var(--primary); color: white; padding: 40px 20px; text-align: center; margin-top: 60px; }}
.footer p {{ opacity: 0.8; font-size: 0.9rem; margin-bottom: 8px; }}
.footer a {{ color: var(--accent-light); text-decoration: none; }}
.footer a:hover {{ text-decoration: underline; }}

/* ─── Responsive ─────────────────────────────────────────── */
@media (max-width: 768px) {{
  .hero h1 {{ font-size: 1.8rem; }}
  .hero p {{ font-size: 1rem; }}
  .hero-stats {{ gap: 20px; }}
  .grid {{ grid-template-columns: 1fr; }}
  .nav-links {{ display: none; }}
  .arch-layer {{ flex-direction: column; }}
  .arch-label {{ min-width: auto; }}
}}
</style>
</head>
<body>

<!-- Navigation -->
<nav class="nav">
  <div class="nav-inner">
    <a href="#" class="nav-logo">🏛️ JuraRegel</a>
    <div class="nav-links">
      <a href="#methodology">Methodologie</a>
      <a href="#calculator">Calculator</a>
      <a href="#templates">Templates</a>
      <a href="#architecture">Architectuur</a>
      <a href="#api">API</a>
    </div>
  </div>
</nav>

<!-- Hero -->
<section class="hero">
  <h1>Living Compliance Engine</h1>
  <p>Van juridische regels naar IT-code. Continue compliance-monitoring met AI-gestuurde analyse, 37 evidence-based templates, en volledige audit-trail.</p>
  <div class="hero-badges">
    <span class="badge">EU AI Act</span>
    <span class="badge">AVG/GDPR</span>
    <span class="badge">ISO 27001</span>
    <span class="badge">IEEE 7000</span>
    <span class="badge">NIST AI RMF</span>
  </div>
  <div class="hero-stats">
    <div class="stat"><div class="stat-value">37</div><div class="stat-label">Templates</div></div>
    <div class="stat"><div class="stat-value">50+</div><div class="stat-label">Use Cases</div></div>
    <div class="stat"><div class="stat-value">4</div><div class="stat-label">Fasen</div></div>
    <div class="stat"><div class="stat-value">12</div><div class="stat-label">Referenties</div></div>
  </div>
</section>

<!-- Methodology Phases -->
<section class="section" id="methodology">
  <div class="container">
    <h2 class="section-title">Continue Compliance Cyclus</h2>
    <p class="section-subtitle">Van registratie tot monitoring — een gesloten lus van continue verbetering</p>
    <div class="phases-grid">
      <div class="phase-card" style="--phase-color: #3182ce">
        <div class="phase-icon">📋</div>
        <div class="phase-title">1. Registreren</div>
        <div class="phase-desc">Verwerkingsactiviteiten registreren in het verwerkingsregister (AVG Art. 30). Automatische detectie van DPIA/FRIA-verplichtingen op basis van 9 EDPB-criteria.</div>
      </div>
      <div class="phase-card" style="--phase-color: #38a169">
        <div class="phase-icon">⚖️</div>
        <div class="phase-title">2. Beoordelen</div>
        <div class="phase-desc">Risico-analyse met 37 evidence-based templates. RAG-gestuurde juridische analyse met bron-citaties en hallucinatie-detectie.</div>
      </div>
      <div class="phase-card" style="--phase-color: #d69e2e">
        <div class="phase-icon">🛡️</div>
        <div class="phase-title">3. Mitigeren</div>
        <div class="phase-desc">Geprioriteerde maatregelen met juridische basis. Workflow-gestuurde implementatie met verantwoordelijkheden en deadlines.</div>
      </div>
      <div class="phase-card" style="--phase-color: #805ad5">
        <div class="phase-icon">📊</div>
        <div class="phase-title">4. Monitoren</div>
        <div class="phase-desc">Continue compliance-monitoring, wetswijzigingsdetectie, en real-time compliance scoring met trend-analyse.</div>
      </div>
    </div>
  </div>
</section>

<!-- Compliance Calculator -->
<section class="section" id="calculator" style="background: white;">
  <div class="container">
    <h2 class="section-title">Compliance Calculator</h2>
    <p class="section-subtitle">Beoordeel snel of een verwerking een DPIA vereist volgens de 9 EDPB-criteria</p>
    <div class="calculator">
      <div class="calc-group">
        <label class="calc-label">Type verwerking</label>
        <select class="calc-select" id="calc-type">
          <option value="standard">Standaard verwerking</option>
          <option value="sensitive">Gevoelige gegevens (Art. 9)</option>
          <option value="large-scale">Grootschalige verwerking</option>
          <option value="innovative">Innovatieve technologie (AI, biometrie)</option>
          <option value="monitoring">Systematische monitoring</option>
          <option value="vulnerable">Kwetsbare betrokkenen</option>
        </select>
      </div>
      <div class="calc-group">
        <label class="calc-label">Aantal betrokkenen</label>
        <select class="calc-select" id="calc-scale">
          <option value="small">&lt; 1.000</option>
          <option value="medium">1.000 - 10.000</option>
          <option value="large">10.000 - 100.000</option>
          <option value="xlarge">&gt; 100.000</option>
        </select>
      </div>
      <div class="calc-group">
        <label class="calc-label">Rechtsgrond</label>
        <select class="calc-select" id="calc-legal">
          <option value="consent">Toestemming (Art. 6(1)(a))</option>
          <option value="contract">Contract (Art. 6(1)(b))</option>
          <option value="legal">Wettelijke verplichting (Art. 6(1)(c))</option>
          <option value="public">Openbaar belang (Art. 6(1)(e))</option>
          <option value="legitimate">Gerechtvaardigd belang (Art. 6(1)(f))</option>
        </select>
      </div>
      <div class="calc-group">
        <label class="calc-label">Geautomatiseerde besluitvorming</label>
        <select class="calc-select" id="calc-automated">
          <option value="no">Nee</option>
          <option value="yes-with-effects">Ja, met juridische/financiële gevolgen</option>
          <option value="yes-profiling">Ja, met profiling</option>
        </select>
      </div>
      <div style="text-align: center; margin-top: 20px;">
        <button onclick="calculateCompliance()" style="background: var(--primary); color: white; border: none; padding: 12px 32px; border-radius: var(--radius-sm); font-size: 1rem; cursor: pointer; font-weight: 600;">Bereken</button>
      </div>
      <div class="calc-result" id="calc-result" style="display: none;">
        <div class="calc-score" id="calc-score">—</div>
        <div class="calc-label-score">Compliance Risico Score</div>
        <div class="calc-verdict" id="calc-verdict">—</div>
      </div>
    </div>
  </div>
</section>

<!-- Templates -->
<section class="section" id="templates">
  <div class="container">
    <h2 class="section-title">37 Compliance Templates</h2>
    <p class="section-subtitle">Evidence-based assessments met juridische onderbouwing</p>
    <div class="controls">
      <input type="text" class="search" id="search" placeholder="Zoek templates..." oninput="filterTemplates()">
      <div class="filter-btns">
        <button class="filter-btn active" onclick="setCategory('all', this)">Alle</button>
        <button class="filter-btn" onclick="setCategory('Privacy', this)">Privacy</button>
        <button class="filter-btn" onclick="setCategory('Informatiebeveiliging', this)">IB</button>
        <button class="filter-btn" onclick="setCategory('AI & Algoritmes', this)">AI</button>
        <button class="filter-btn" onclick="setCategory('Fase 1 — Wettelijk Kritiek', this)">Fase 1</button>
        <button class="filter-btn" onclick="setCategory('Fase 2 — Methodologisch', this)">Fase 2</button>
        <button class="filter-btn" onclick="setCategory('Fase 3 — Academisch Diep', this)">Fase 3</button>
      </div>
    </div>
    <div class="grid" id="grid"></div>
  </div>
</section>

<!-- Architecture -->
<section class="section" id="architecture" style="background: white;">
  <div class="container">
    <h2 class="section-title">Architectuur</h2>
    <p class="section-subtitle">Living Compliance Engine — van presentatie tot data-laag</p>
    <div class="arch-diagram">
      <div class="arch-layer">
        <div class="arch-label">Presentatie</div>
        <div class="arch-boxes">
          <div class="arch-box">Dashboard</div>
          <div class="arch-box">Assessment Workspace</div>
          <div class="arch-box">Regulatory Monitor</div>
          <div class="arch-box">Audit Console</div>
        </div>
      </div>
      <div class="arch-layer">
        <div class="arch-label">API</div>
        <div class="arch-boxes">
          <div class="arch-box">REST (OpenAPI 3.1)</div>
          <div class="arch-box">GraphQL</div>
          <div class="arch-box">OAuth2 + mTLS</div>
          <div class="arch-box">Rate Limiting</div>
        </div>
      </div>
      <div class="arch-layer">
        <div class="arch-label">Core Services</div>
        <div class="arch-boxes">
          <div class="arch-box core">Template Service</div>
          <div class="arch-box core">Assessment Engine</div>
          <div class="arch-box core">Evidence Service</div>
          <div class="arch-box core">Workflow Engine</div>
          <div class="arch-box core">Compliance Scoring</div>
        </div>
      </div>
      <div class="arch-layer">
        <div class="arch-label">AI / LLM</div>
        <div class="arch-boxes">
          <div class="arch-box ai">RAG Pipeline</div>
          <div class="arch-box ai">Knowledge Graph (NMF)</div>
          <div class="arch-box ai">Legal Reasoning</div>
          <div class="arch-box ai">Hallucination Detection</div>
        </div>
      </div>
      <div class="arch-layer">
        <div class="arch-label">Data</div>
        <div class="arch-boxes">
          <div class="arch-box data">PostgreSQL</div>
          <div class="arch-box data">Qdrant (Vectors)</div>
          <div class="arch-box data">Redis (Cache)</div>
          <div class="arch-box data">Immutable Audit Log</div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- API Preview -->
<section class="section" id="api">
  <div class="container">
    <h2 class="section-title">API</h2>
    <p class="section-subtitle">REST + GraphQL voor integratie met bestaande systemen</p>
    <div style="background: var(--card-bg); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow); overflow-x: auto;">
      <pre style="font-family: 'Fira Code', monospace; font-size: 0.85rem; line-height: 1.6;"><code><span style="color: #38a169;">GET</span>  /api/v1/templates/              <span style="color: #718096;"># 37 templates</span>
<span style="color: #38a169;">POST</span> /api/v1/templates/{id}/generate  <span style="color: #718096;"># Genereer document</span>
<span style="color: #38a169;">POST</span> /api/v1/templates/{id}/render    <span style="color: #718096;"># Render markdown/html/json</span>

<span style="color: #3182ce;">POST</span> /api/v1/assessments/             <span style="color: #718096;"># Create assessment</span>
<span style="color: #3182ce;">POST</span> /api/v1/assessments/{id}/submit  <span style="color: #718096;"># Submit for review</span>
<span style="color: #3182ce;">POST</span> /api/v1/assessments/{id}/approve <span style="color: #718096;"># Approve (FG role)</span>
<span style="color: #3182ce;">POST</span> /api/v1/assessments/{id}/publish <span style="color: #718096;"># Publish</span>

<span style="color: #805ad5;">POST</span> /api/v1/processing-activities/  <span style="color: #718096;"># Register verwerking</span>
<span style="color: #805ad5;">GET</span>  /api/v1/evidence/{id}/coverage  <span style="color: #718096;"># Evidence coverage</span></code></pre>
    </div>
  </div>
</section>

<!-- Footer -->
<footer class="footer">
  <p><strong>JuraRegel</strong> — Living Compliance Engine</p>
  <p>37 templates · 50+ use-cases · 4 fasen · 12 academische referenties</p>
  <p style="margin-top: 16px;">
    <a href="https://github.com/djimit/juraregel">GitHub</a> &nbsp;|&nbsp;
    <a href="https://github.com/djimit/juraregel/blob/main/docs/JURATOOL-LEVEL3-ARCHITECTURE.md">Level 3 Architecture</a> &nbsp;|&nbsp;
    <a href="https://github.com/djimit/juraregel/blob/main/docs/JURATOOL-NEXT-STEP-ARCHITECTURE.md">Next-Step Roadmap</a>
  </p>
  <p style="margin-top: 16px; font-size: 0.8rem; opacity: 0.6;">
    IEEE 7000-2021 · NIST AI RMF · EU AI Act · AVG · ISO 27005 · CNIL PIA · EDPB WP29
  </p>
</footer>

<!-- Modal -->
<div class="modal-overlay" id="modal" onclick="closeModal(event)">
  <div class="modal" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h2 id="modal-title"></h2>
      <div class="meta" id="modal-meta"></div>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body" id="modal-body"></div>
  </div>
</div>

<script>
const TEMPLATES = {templates_json};

// Stats
const withCheckboxes = TEMPLATES.filter(t => t.has_checkboxes).length;
const withScoring = TEMPLATES.filter(t => t.has_scoring).length;

// State
let currentCategory = 'all';
let searchQuery = '';

// Render grid
function renderGrid() {{
  const grid = document.getElementById('grid');
  grid.innerHTML = '';

  const filtered = TEMPLATES.filter(t => {{
    const matchCat = currentCategory === 'all' || t.category === currentCategory;
    const matchSearch = !searchQuery ||
      t.document.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.wettelijke_basis.toLowerCase().includes(searchQuery.toLowerCase());
    return matchCat && matchSearch;
  }});

  filtered.forEach(t => {{
    const card = document.createElement('div');
    card.className = 'card';
    card.onclick = () => openModal(t.id);

    const tags = [];
    if (t.has_checkboxes) tags.push('<span class="tag">☑ Interactief</span>');
    if (t.has_scoring) tags.push('<span class="tag scoring">📊 Scoring</span>');
    tags.push(`<span class="tag">${{t.section_count}} secties</span>`);

    card.innerHTML = `
      <div class="card-category">${{t.category}}</div>
      <div class="card-title">${{t.document}}</div>
      <div class="card-meta">${{t.wettelijke_basis}}${{t.model_versie ? ' · v' + t.model_versie : ''}}</div>
      <div class="card-tags">${{tags.join(' ')}}</div>
    `;
    grid.appendChild(card);
  }});

  if (filtered.length === 0) {{
    grid.innerHTML = '<p style="color: var(--text-light); padding: 40px; text-align: center; grid-column: 1/-1;">Geen templates gevonden.</p>';
  }}
}}

function filterTemplates() {{
  searchQuery = document.getElementById('search').value;
  renderGrid();
}}

function setCategory(cat, btn) {{
  currentCategory = cat;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderGrid();
}}

function openModal(docId) {{
  const t = TEMPLATES.find(x => x.id === docId);
  if (!t) return;

  document.getElementById('modal-title').textContent = t.document;
  document.getElementById('modal-meta').textContent =
    `${{t.wettelijke_basis}} · ${{t.section_count}} secties · ${{t.category}}`;
  document.getElementById('modal-body').innerHTML = markdownToHtml(t.markdown);
  document.getElementById('modal').classList.add('active');
  document.body.style.overflow = 'hidden';
}}

function closeModal(e) {{
  if (e && e.target !== e.currentTarget) return;
  document.getElementById('modal').classList.remove('active');
  document.body.style.overflow = '';
}}

function markdownToHtml(md) {{
  const lines = md.split('\\n');
  let html = '';
  let inList = false;

  for (const line of lines) {{
    const s = line.trim();
    if (!s) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      continue;
    }}
    if (s.startsWith('# ')) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      html += `<h2>${{escapeHtml(s.slice(2))}}</h2>`;
    }} else if (s.startsWith('## ')) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      html += `<h3>${{escapeHtml(s.slice(3))}}</h3>`;
    }} else if (s.startsWith('### ')) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      html += `<h4>${{escapeHtml(s.slice(4))}}</h4>`;
    }} else if (s.startsWith('---')) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      html += '<hr>';
    }} else if (s.startsWith('- ')) {{
      if (!inList) {{ html += '<ul>'; inList = true; }}
      html += `<li>${{formatInline(s.slice(2))}}</li>`;
    }} else {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      html += `<p>${{formatInline(s)}}</p>`;
    }}
  }}
  if (inList) html += '</ul>';
  return html;
}}

function formatInline(text) {{
  text = escapeHtml(text);
  text = text.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
  text = text.replace(/\\*(.+?)\\*/g, '<em>$1</em>');
  return text;
}}

function escapeHtml(text) {{
  return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}}

// Compliance Calculator
function calculateCompliance() {{
  const type = document.getElementById('calc-type').value;
  const scale = document.getElementById('calc-scale').value;
  const legal = document.getElementById('calc-legal').value;
  const automated = document.getElementById('calc-automated').value;

  let score = 0;
  let maxScore = 0;

  // Type scoring (0-30)
  maxScore += 30;
  if (type === 'sensitive') score += 30;
  else if (type === 'innovative') score += 25;
  else if (type === 'monitoring') score += 25;
  else if (type === 'vulnerable') score += 20;
  else if (type === 'large-scale') score += 15;
  else score += 5;

  // Scale scoring (0-25)
  maxScore += 25;
  if (scale === 'xlarge') score += 25;
  else if (scale === 'large') score += 20;
  else if (scale === 'medium') score += 10;
  else score += 5;

  // Legal basis scoring (0-20)
  maxScore += 20;
  if (legal === 'legitimate') score += 15;
  else if (legal === 'consent') score += 10;
  else if (legal === 'public') score += 10;
  else score += 5;

  // Automated decision scoring (0-25)
  maxScore += 25;
  if (automated === 'yes-with-effects') score += 25;
  else if (automated === 'yes-profiling') score += 20;
  else score += 0;

  const normalized = Math.round((score / maxScore) * 100);

  let verdict, color;
  if (normalized >= 75) {{ verdict = '🔴 DPIA Verplicht'; color = '#e53e3e'; }}
  else if (normalized >= 50) {{ verdict = '🟠 DPIA Waarschijnlijk Verplicht'; color = '#dd6b20'; }}
  else if (normalized >= 25) {{ verdict = '🟡 Pre-scan Aanbevolen'; color: '#d69e2e'; }}
  else {{ verdict = '🟢 DPIA Niet Verplicht'; color = '#38a169'; }}

  document.getElementById('calc-result').style.display = 'block';
  document.getElementById('calc-score').textContent = normalized;
  document.getElementById('calc-score').style.color = color;
  const vEl = document.getElementById('calc-verdict');
  vEl.textContent = verdict;
  vEl.style.background = color + '20';
  vEl.style.color = color;
}}

// Close on Escape
document.addEventListener('keydown', e => {{
  if (e.key === 'Escape') closeModal();
}});

// Initial render
renderGrid();
</script>
</body>
</html>"""


if __name__ == "__main__":
    generate_demo()
