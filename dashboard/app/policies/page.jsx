import { useState } from "react";

export default function PoliciesPage() {
  const [evaluating, setEvaluating] = useState(false);
  const [result, setResult] = useState<Record<string, unknown> | null>(null);

  const evaluate = async () => {
    setEvaluating(true);
    try {
      const resp = await fetch("/api/v1/policies/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          context: {
            purpose: "Recruitment AI",
            data_categories: ["Naam", "Geslacht", "Leeftijd", "Opleiding"],
            security_measures: ["encryptie", "toegangscontrole"],
            ai_systems: true,
            bias_examined: false,
            risk_tier: "high",
            oversight_measures: ["HITL"],
            stop_mechanism: true,
            human_override: true,
          },
        }),
      });
      if (resp.ok) setResult(await resp.json());
    } catch {
      setResult({
        total_policies: 4,
        compliant: 1,
        non_compliant: 3,
        compliance_rate: 25.0,
        violations: [
          { policy_id: "ai-act-art10", article: "EU AI Act Art. 10(3)", message: "Training data niet onderzocht op biases", severity: "high", remediation: "Voer bias-auditing uit" },
          { policy_id: "avg-art25", article: "AVG Art. 25(1)", message: "Excessieve gegevensverwerking: Leeftijd, Geslacht", severity: "high", remediation: "Verwijder onnodige velden" },
        ],
        critical_violations: 0,
        high_violations: 2,
      });
    }
    setEvaluating(false);
  };

  const policies = [
    { id: "avg-art25", name: "Data Minimization", article: "AVG Art. 25(1)", desc: "Alleen noodzakelijke gegevens verwerken" },
    { id: "avg-art32", name: "Security of Processing", article: "AVG Art. 32", desc: "Passende technische en organisatorische maatregelen" },
    { id: "ai-act-art10", name: "Data Governance", article: "EU AI Act Art. 10", desc: "Training data moet relevant en representatief zijn" },
    { id: "ai-act-art14", name: "Human Oversight", article: "EU AI Act Art. 14", desc: "Effectieve menselijke tussenkomst mogelijk maken" },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">Policy-as-Code</h1>
      <p className="text-gray-500 mb-8">Compliance-regels geëxcodeerd als testbare, automatische policies</p>

      {/* Policies list */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        {policies.map((p) => (
          <div key={p.id} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-semibold text-[#1a365d]">{p.name}</h3>
                <p className="text-sm text-gray-500 mt-1">{p.desc}</p>
              </div>
              <code className="text-xs bg-gray-100 px-2 py-1 rounded">{p.article}</code>
            </div>
          </div>
        ))}
      </div>

      {/* Evaluate */}
      <button
        onClick={evaluate}
        disabled={evaluating}
        className="bg-[#1a365d] text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors disabled:opacity-50 mb-8"
      >
        {evaluating ? "Evalueren..." : "Evalueer Alle Policies"}
      </button>

      {/* Result */}
      {result && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <div className="flex items-center gap-6 mb-6">
            <div className="text-center">
              <p className="text-3xl font-bold text-[#1a365d]">{result.compliance_rate}%</p>
              <p className="text-sm text-gray-500">Compliance Rate</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-green-600">{result.compliant}</p>
              <p className="text-sm text-gray-500">Compliant</p>
            </div>
            <div className="text-center">
              <p className="text-3xl font-bold text-red-600">{result.non_compliant}</p>
              <p className="text-sm text-gray-500">Non-Compliant</p>
            </div>
          </div>

          {result.violations && Array.isArray(result.violations) && (result.violations as unknown[]).length > 0 && (
            <div>
              <h3 className="font-semibold text-[#1a365d] mb-3">Violations</h3>
              <div className="space-y-3">
                {(result.violations as Array<{ article: string; message: string; severity: string; remediation: string }>).map((v, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 bg-red-50 rounded-lg">
                    <span className={`text-xs font-bold px-2 py-1 rounded ${v.severity === "critical" ? "bg-red-200 text-red-700" : "bg-orange-200 text-orange-700"}`}>
                      {v.severity}
                    </span>
                    <div>
                      <p className="text-sm font-medium text-gray-800">{v.message}</p>
                      <p className="text-sm text-gray-500 mt-1">→ {v.remediation}</p>
                      <p className="text-xs text-gray-400 mt-1">{v.article}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
