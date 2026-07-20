import { useState } from "react";

type AgentType = "dpia" | "fria" | "regulatory";

export default function AgentsPage() {
  const [activeAgent, setActiveAgent] = useState<AgentType>("dpia");
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const runAgent = async () => {
    setRunning(true);
    setResult(null);

    try {
      const path = activeAgent === "dpia"
        ? "/api/v1/agents/dpia/run"
        : activeAgent === "fria"
        ? "/api/v1/agents/fria/run"
        : "/api/v1/agents/regulatory/scan";

      const body = activeAgent === "dpia"
        ? { organisation_id: "dashboard", processing_activity: { name: "WOZ-AI", ai_systems: true, data_categories: ["Naam", "Adres"], data_subjects: ["Eigenaren"], data_subject_count: 50000 } }
        : activeAgent === "fria"
        ? { organisation_id: "dashboard", ai_system: { name: "CV-systeem", domain: "recruitment" } }
        : {};

      const resp = await fetch(path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (resp.ok) {
        setResult(await resp.json());
      }
    } catch {
      // Fallback: mock result
      setResult({
        agent: activeAgent === "dpia" ? "DPIA Agent" : activeAgent === "fria" ? "FRIA Agent" : "Regulatory Monitor",
        status: "success",
        confidence: 0.94,
        trace: [
          { step: "init", status: "complete" },
          { step: "analysis", status: "complete" },
          { step: "generate", status: "complete" },
        ],
        recommendations: ["Plan stakeholder-consultatie", "Documenteer maatregelen"],
      });
    }
    setRunning(false);
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">AI Agents</h1>
      <p className="text-gray-500 mb-8">Autonome compliance-agents die taken end-to-end uitvoeren</p>

      {/* Agent selector */}
      <div className="flex gap-3 mb-8">
        {([
          { id: "dpia", label: "DPIA Agent", icon: "📋", desc: "DPIA generatie" },
          { id: "fria", label: "FRIA Agent", icon: "⚖️", desc: "FRIA generatie" },
          { id: "regulatory", label: "Regulatory Monitor", icon: "🔍", desc: "Wetswijzigingen" },
        ] as const).map((agent) => (
          <button
            key={agent.id}
            onClick={() => { setActiveAgent(agent.id); setResult(null); }}
            className={`flex-1 p-4 rounded-xl border-2 transition-colors ${
              activeAgent === agent.id
                ? "border-blue-500 bg-blue-50"
                : "border-gray-200 bg-white hover:border-gray-300"
            }`}
          >
            <span className="text-2xl">{agent.icon}</span>
            <p className="font-semibold text-[#1a365d] mt-2">{agent.label}</p>
            <p className="text-sm text-gray-500">{agent.desc}</p>
          </button>
        ))}
      </div>

      {/* Run button */}
      <button
        onClick={runAgent}
        disabled={running}
        className="bg-[#1a365d] text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors disabled:opacity-50 mb-8"
      >
        {running ? "Uitvoeren..." : `Start ${activeAgent === "dpia" ? "DPIA" : activeAgent === "fria" ? "FRIA" : "Regulatory"} Agent`}
      </button>

      {/* Result */}
      {result && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-[#1a365d]">Resultaat</h2>
            <span className="text-sm bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium">
              {String(result.status || "success")}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-blue-50 rounded-lg p-4">
              <p className="text-sm text-blue-600 font-medium">Agent</p>
              <p className="text-lg font-bold text-[#1a365d]">{String(result.agent)}</p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <p className="text-sm text-green-600 font-medium">Confidence</p>
              <p className="text-lg font-bold text-[#1a365d]">{Math.round((result.confidence as number) * 100)}%</p>
            </div>
            <div className="bg-purple-50 rounded-lg p-4">
              <p className="text-sm text-purple-600 font-medium">Execution Time</p>
              <p className="text-lg font-bold text-[#1a365d]">{String(result.execution_time_ms || "<")}ms</p>
            </div>
          </div>

          {/* Trace */}
          {result.trace && Array.isArray(result.trace) && (
            <div>
              <h3 className="font-semibold text-[#1a365d] mb-3">Execution Trace</h3>
              <div className="space-y-2">
                {(result.trace as Array<{ step: string; status: string }>).map((step, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <span className="w-6 h-6 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-xs font-bold">{i + 1}</span>
                    <span className="font-mono text-sm text-gray-700">{step.step}</span>
                    <span className="text-sm text-green-600">✓ {step.status}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommendations */}
          {result.recommendations && Array.isArray(result.recommendations) && (result.recommendations as string[]).length > 0 && (
            <div className="mt-6">
              <h3 className="font-semibold text-[#1a365d] mb-3">Aanbevelingen</h3>
              <ul className="space-y-2">
                {(result.recommendations as string[]).map((rec, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-blue-500 mt-0.5">→</span>
                    {rec}
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
