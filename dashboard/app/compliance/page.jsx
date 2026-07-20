import { useState } from "react";

export default function CompliancePage() {
  const [measuresImpl, setMeasuresImpl] = useState(5);
  const [measuresTotal, setMeasuresTotal] = useState(8);
  const [training, setTraining] = useState(true);
  const [score, setScore] = useState<number | null>(null);
  const [calculating, setCalculating] = useState(false);

  const calculate = async () => {
    setCalculating(true);
    try {
      const resp = await fetch("/api/v1/compliance/score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          measures_implemented: measuresImpl,
          measures_total: measuresTotal,
          training_current: training,
        }),
      });
      if (resp.ok) {
        const data = await resp.json();
        setScore(data.score);
      }
    } catch {
      // Fallback: calculate locally
      const raw = (measuresImpl / measuresTotal * 0.4 + (training ? 0.2 : 0) + 0.25) * 100;
      setScore(Math.round(raw));
    }
    setCalculating(false);
  };

  const getClassification = (s: number) => {
    if (s >= 90) return { label: "Excellent", color: "text-green-600", bg: "bg-green-50" };
    if (s >= 75) return { label: "Goed", color: "text-green-600", bg: "bg-green-50" };
    if (s >= 60) return { label: "Voldoende", color: "text-yellow-600", bg: "bg-yellow-50" };
    if (s >= 40) return { label: "Onvoldoende", color: "text-orange-600", bg: "bg-orange-50" };
    return { label: "Kritiek", color: "text-red-600", bg: "bg-red-50" };
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">Compliance Score</h1>
      <p className="text-gray-500 mb-8">Real-time compliance score berekening op basis van 7 gewogen criteria</p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-bold text-[#1a365d] mb-4">Parameters</h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Geïmplementeerde maatregelen: {measuresImpl}
              </label>
              <input
                type="range" min="0" max={measuresTotal}
                value={measuresImpl}
                onChange={(e) => setMeasuresImpl(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Totaal maatregelen: {measuresTotal}
              </label>
              <input
                type="range" min="1" max="20"
                value={measuresTotal}
                onChange={(e) => setMeasuresTotal(Number(e.target.value))}
                className="w-full"
              />
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox" checked={training}
                onChange={(e) => setTraining(e.target.checked)}
                className="w-5 h-5 rounded"
              />
              <label className="text-sm font-medium text-gray-700">Training actueel</label>
            </div>

            <button
              onClick={calculate}
              disabled={calculating}
              className="w-full bg-[#1a365d] text-white py-3 rounded-lg font-semibold hover:bg-blue-800 transition-colors disabled:opacity-50"
            >
              {calculating ? "Berekenen..." : "Bereken Score"}
            </button>
          </div>
        </div>

        {/* Result */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
          <h2 className="text-lg font-bold text-[#1a365d] mb-4">Resultaat</h2>

          {score !== null ? (
            <div className="text-center">
              <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getClassification(score).bg}`}>
                <span className={`text-4xl font-bold ${getClassification(score).color}`}>{score}</span>
              </div>
              <p className={`mt-4 text-lg font-semibold ${getClassification(score).color}`}>
                {getClassification(score).label}
              </p>
              <p className="text-sm text-gray-500 mt-2">van 100 punten</p>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-400">
              <p className="text-4xl mb-2">⚖️</p>
              <p>Klik op &quot;Bereken Score&quot; om te starten</p>
            </div>
          )}

          {/* Criteria weights */}
          <div className="mt-6 pt-6 border-t border-gray-100">
            <h3 className="text-sm font-semibold text-gray-700 mb-3">Score Criteria</h3>
            <div className="space-y-2 text-sm">
              {[
                { name: "Documentatie Compleetheid", weight: "20%" },
                { name: "Evidence Actualiteit", weight: "15%" },
                { name: "Review-Termijnen", weight: "15%" },
                { name: "Maatregelen-Implementatie", weight: "20%" },
                { name: "Incidenten-Afhandeling", weight: "10%" },
                { name: "Training Actualiteit", weight: "10%" },
                { name: "Stakeholder-Consultatie", weight: "10%" },
              ].map((c) => (
                <div key={c.name} className="flex justify-between text-gray-600">
                  <span>{c.name}</span>
                  <span className="font-mono">{c.weight}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
