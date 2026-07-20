"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

export default function DashboardPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [name, setName] = useState("WOZ-AI Waardering");
  const [aiSystems, setAiSystems] = useState(true);
  const [dataSubjectCount, setDataSubjectCount] = useState(10000);

  const runAssessment = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const resp = await fetch(`${API_URL}/api/v1/orchestrator/assess`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          organisation_id: "demo",
          processing_activity: {
            name: name,
            ai_systems: aiSystems,
            data_categories: ["Naam", "Adres", "WOZ-waarde"],
            data_subjects: ["Eigenaren"],
            data_subject_count: dataSubjectCount,
            security_measures: ["encryptie"],
          },
        }),
      });

      if (!resp.ok) throw new Error(`API error: ${resp.status}`);
      setResult(await resp.json());
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">
        🏛️ JuraRegel Compliance Agent
      </h1>
      <p className="text-gray-500 mb-8">
        Autonome juridische analyse — van verwerkingsregister tot compliance-assessment
      </p>

      {/* Input */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 mb-8">
        <h2 className="text-lg font-bold text-[#1a365d] mb-4">
          Verwerkingsactiviteit
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Naam</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Aantal betrokkenen: {dataSubjectCount}
            </label>
            <input
              type="range"
              min="100"
              max="100000"
              step="100"
              value={dataSubjectCount}
              onChange={(e) => setDataSubjectCount(Number(e.target.value))}
              className="w-full"
            />
          </div>
          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              checked={aiSystems}
              onChange={(e) => setAiSystems(e.target.checked)}
              className="w-5 h-5 rounded"
            />
            <label className="text-sm font-medium text-gray-700">
              AI-systeem (valt onder EU AI Act)
            </label>
          </div>
        </div>
        <button
          onClick={runAssessment}
          disabled={loading}
          className="mt-6 bg-[#1a365d] text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors disabled:opacity-50"
        >
          {loading ? "Analyse läuft..." : "Start Autonome Analyse"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-8">
          <p className="text-red-700 font-medium">Fout: {error}</p>
        </div>
      )}

      {/* Result */}
      {result && (
        <div className="space-y-6">
          {/* Summary */}
          <div className={`rounded-xl p-6 shadow-sm border ${
            result.human_review_required
              ? "bg-yellow-50 border-yellow-200"
              : "bg-green-50 border-green-200"
          }`}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-[#1a365d]">Conclusie</h2>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                result.confidence >= 0.7
                  ? "bg-green-200 text-green-800"
                  : result.confidence >= 0.5
                  ? "bg-yellow-200 text-yellow-800"
                  : "bg-red-200 text-red-800"
              }`}>
                Confidence: {Math.round(result.confidence * 100)}%
              </span>
            </div>
            <p className="text-gray-800">{result.conclusion}</p>
            {result.human_review_required && (
              <p className="text-yellow-700 mt-3 text-sm font-medium">
                ⚠️ Menselijke review vereist — confidence te laag of gevonden gaps
              </p>
            )}
          </div>

          {/* Analysis Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500">Frameworks</p>
              <p className="text-2xl font-bold text-[#1a365d]">
                {result.analysis_summary?.jurisdictions?.length || 0}
              </p>
            </div>
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500">Verplichtingen</p>
              <p className="text-2xl font-bold text-[#1a365d]">
                {result.analysis_summary?.obligations || 0}
              </p>
            </div>
            <div className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <p className="text-sm text-gray-500">Risico's</p>
              <p className="text-2xl font-bold text-[#1a365d]">
                {result.analysis_summary?.risks || 0}
              </p>
            </div>
          </div>

          {/* Steps */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
            <h2 className="text-lg font-bold text-[#1a365d] mb-4">
              Analysis Steps
            </h2>
            <div className="space-y-2">
              {result.steps?.map((step, i) => (
                <div key={i} className="flex items-center gap-3">
                  <span className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                    step.status === "completed"
                      ? "bg-green-100 text-green-600"
                      : "bg-red-100 text-red-600"
                  }`}>
                    {i + 1}
                  </span>
                  <span className="font-mono text-sm text-gray-700">{step.name}</span>
                  <span className="text-sm text-gray-400">{step.duration_ms}ms</span>
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-400 mt-4">
              Total: {result.total_duration_ms}ms | Model: {result.model_used}
            </p>
          </div>

          {/* Required Actions */}
          {result.required_actions?.length > 0 && (
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <h2 className="text-lg font-bold text-[#1a365d] mb-4">
                Vereiste Acties
              </h2>
              <ul className="space-y-2">
                {result.required_actions.map((action, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-blue-500 mt-0.5">→</span>
                    {action}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
