#!/usr/bin/env python3
"""Generate static JuraRegel Template Demo for GitHub Pages.

Reads all 37 templates, renders them to HTML, and produces a single
self-contained index.html that can be served by GitHub Pages.

Usage:
    python demo/generate_static_demo.py
    # Output: demo/index.html (replaces old demo)
"""

import json
import sys
from pathlib import Path

# Setup path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from docs.templates import generate_document, enrich_document, list_documents
from docs.templates.render_engine import render_document
from docs.templates.template_schema import get_template_info


# ─── Template categories ──────────────────────────────────────

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


def get_category(doc_id: str) -> str:
    for cat, ids in CATEGORIES.items():
        if doc_id in ids:
            return cat
    return "Overig"


def generate_demo():
    """Generate the full static demo HTML."""
    documents = list_documents()

    # Build template data
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
                    "bron": enriched.get("bron", ""),
                    "section_count": info["section_count"],
                    "has_checkboxes": info["has_checkboxes"],
                    "has_scoring": info["has_scoring"],
                    "markdown": md,
                }
            )
        except Exception as e:
            print(f"  Warning: {doc_id} skipped: {e}")

    # Generate HTML
    html = _build_html(templates_data)

    # Write
    output_path = ROOT / "demo" / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Generated demo: {output_path}")
    print(f"   Templates: {len(templates_data)}")
    print(f"   File size: {len(html):,} bytes")


def _build_html(templates: list[dict]) -> str:
    """Build the full demo HTML page."""
    templates_json = json.dumps(templates, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JuraRegel — Template Demo</title>
<style>
:root {{
  --primary: #1a365d;
  --primary-light: #2b6cb0;
  --accent: #38a169;
  --bg: #f7fafc;
  --card-bg: #ffffff;
  --text: #2d3748;
  --text-light: #718096;
  --border: #e2e8f0;
  --shadow: 0 1px 3px rgba(0,0,0,0.1);
  --radius: 8px;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}

/* Header */
.header {{ background: linear-gradient(135deg, var(--primary), var(--primary-light)); color: white; padding: 30px; border-radius: var(--radius); margin-bottom: 24px; }}
.header h1 {{ font-size: 1.8rem; margin-bottom: 8px; }}
.header p {{ opacity: 0.9; font-size: 1rem; }}
.header-stats {{ display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap; }}
.stat {{ text-align: center; }}
.stat-value {{ font-size: 1.5rem; font-weight: 700; }}
.stat-label {{ font-size: 0.8rem; opacity: 0.8; }}

/* Controls */
.controls {{ display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; align-items: center; }}
.search {{ flex: 1; min-width: 200px; padding: 10px 16px; border: 1px solid var(--border); border-radius: var(--radius); font-size: 0.95rem; }}
.search:focus {{ outline: none; border-color: var(--primary-light); }}
.filter-btn {{ padding: 8px 16px; border: 1px solid var(--border); background: var(--card-bg); border-radius: var(--radius); cursor: pointer; font-size: 0.85rem; transition: all 0.2s; }}
.filter-btn:hover {{ border-color: var(--primary-light); }}
.filter-btn.active {{ background: var(--primary); color: white; border-color: var(--primary); }}

/* Template grid */
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.card {{ background: var(--card-bg); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow); cursor: pointer; transition: all 0.2s; border: 2px solid transparent; }}
.card:hover {{ border-color: var(--primary-light); transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }}
.card-category {{ font-size: 0.75rem; color: var(--primary-light); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
.card-title {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 6px; color: var(--primary); }}
.card-meta {{ font-size: 0.8rem; color: var(--text-light); margin-bottom: 8px; }}
.card-tags {{ display: flex; gap: 6px; flex-wrap: wrap; }}
.tag {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; background: #ebf8ff; color: var(--primary-light); }}
.tag.scoring {{ background: #f0fff4; color: var(--accent); }}

/* Modal */
.modal-overlay {{ display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.6); z-index: 1000; overflow-y: auto; }}
.modal-overlay.active {{ display: flex; justify-content: center; padding: 40px 20px; }}
.modal {{ background: var(--card-bg); border-radius: var(--radius); max-width: 900px; width: 100%; max-height: 85vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
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
.modal-body code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9rem; }}

/* Footer */
.footer {{ text-align: center; padding: 20px; color: var(--text-light); font-size: 0.85rem; }}

/* Responsive */
@media (max-width: 768px) {{
  .grid {{ grid-template-columns: 1fr; }}
  .header h1 {{ font-size: 1.4rem; }}
}}
</style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>🏛️ JuraRegel Template Demo</h1>
    <p>37 compliance templates — Privacy, AI Act, Informatiebeveiliging, Ethiek & meer</p>
    <div class="header-stats">
      <div class="stat"><div class="stat-value" id="stat-total">37</div><div class="stat-label">Templates</div></div>
      <div class="stat"><div class="stat-value" id="stat-categories">7</div><div class="stat-label">Categorieën</div></div>
      <div class="stat"><div class="stat-value" id="stat-checkboxes">—</div><div class="stat-label">Met checkboxes</div></div>
      <div class="stat"><div class="stat-value" id="stat-scoring">—</div><div class="stat-label">Met scoring</div></div>
    </div>
  </div>

  <div class="controls">
    <input type="text" class="search" id="search" placeholder="Zoek templates..." oninput="filterTemplates()">
    <button class="filter-btn active" onclick="setCategory('all')">Alle</button>
    <button class="filter-btn" onclick="setCategory('Privacy')">Privacy</button>
    <button class="filter-btn" onclick="setCategory('Informatiebeveiliging')">IB</button>
    <button class="filter-btn" onclick="setCategory('AI & Algoritmes')">AI</button>
    <button class="filter-btn" onclick="setCategory('Fase 1 — Wettelijk Kritiek')">Fase 1</button>
    <button class="filter-btn" onclick="setCategory('Fase 2 — Methodologisch')">Fase 2</button>
    <button class="filter-btn" onclick="setCategory('Fase 3 — Academisch Diep')">Fase 3</button>
  </div>

  <div class="grid" id="grid"></div>

  <div class="footer">
    <p>JuraRegel v1.0 — Gegenereerd met de Document Rendering Engine</p>
    <p>IEEE 7000-2021 · NIST AI RMF · EU AI Act · AVG · ISO 27005 · CNIL PIA</p>
  </div>
</div>

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
document.getElementById('stat-checkboxes').textContent = withCheckboxes;
document.getElementById('stat-scoring').textContent = withScoring;

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

function setCategory(cat) {{
  currentCategory = cat;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
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
    }} else if (s.startsWith('|')) {{
      if (inList) {{ html += '</ul>'; inList = false; }}
      // Skip table rendering for simplicity
      html += `<code style="display:block;white-space:pre;overflow-x:auto;font-size:0.8rem;background:#f8f8f8;padding:8px;border-radius:4px;margin:8px 0;">${{escapeHtml(s)}}</code>`;
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
