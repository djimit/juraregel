"use client";

const categories = [
  {
    name: "Privacy",
    templates: ["dpia", "privacyverklaring", "verwerkersovereenkomst", "rova", "datalek_procedure", "toestemmingsregister"],
    color: "border-blue-500",
  },
  {
    name: "Informatiebeveiliging",
    templates: ["ib_beleid", "statement_of_applicability", "risicoanalyse", "bcp", "incident_response"],
    color: "border-green-500",
  },
  {
    name: "AI & Algoritmes",
    templates: ["fria", "algoritmeregister", "technische_documentatie_ai", "dpia_rijksdienst", "iama", "fria_eu"],
    color: "border-purple-500",
  },
  {
    name: "Fase 1 — Wettelijk Kritiek",
    templates: ["dpia_pre_scan", "lia", "tia", "ai_risicoclassificatie", "privacy_by_design"],
    color: "border-yellow-500",
  },
  {
    name: "Fase 2 — Methodologisch",
    templates: ["dpia_fria_overlap", "risico_methodiek", "bias_audit", "human_oversight", "bewaarbeleid"],
    color: "border-orange-500",
  },
  {
    name: "Fase 3 — Academisch Diep",
    templates: ["ethics_by_design", "value_sensitive_design", "nist_ai_rmf", "stakeholder_consultatie", "dpia_review"],
    color: "border-red-500",
  },
];

export default function TemplatesPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">Templates</h1>
      <p className="text-gray-500 mb-8">37 evidence-based compliance templates</p>

      <div className="mb-6 bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div className="flex items-center gap-4 text-sm">
          <span className="font-semibold text-[#1a365d]">Totaal: 37 templates</span>
          <span className="text-gray-300">|</span>
          <span className="text-gray-500">7 categorieën</span>
          <span className="text-gray-300">|</span>
          <span className="text-gray-500">AVG + EU AI Act + ISO 27001 + IEEE 7000</span>
        </div>
      </div>

      <div className="space-y-6">
        {categories.map((cat) => (
          <div key={cat.name} className={`bg-white rounded-xl p-6 shadow-sm border-l-4 ${cat.color}`}>
            <h3 className="font-bold text-[#1a365d] mb-3">{cat.name}</h3>
            <div className="flex flex-wrap gap-2">
              {cat.templates.map((t) => (
                <code key={t} className="text-xs bg-gray-100 text-gray-700 px-3 py-1.5 rounded-lg font-mono">
                  {t}
                </code>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
