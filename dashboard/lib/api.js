/**
 * JuraRegel API Client
 * Connects to the JuraRegel REST API.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

async function apiFetch(path, options) {
  if (!API_URL) throw new Error("API_URL not configured");
  const resp = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

export const api = {
  getTemplates: () => apiFetch("/api/v1/templates/"),
  generateTemplate: (id, params) =>
    apiFetch(`/api/v1/templates/${id}/generate`, {
      method: "POST",
      body: JSON.stringify({ organisation: "Dashboard", parameters: params }),
    }),
  getScore: (data) =>
    apiFetch("/api/v1/compliance/score", { method: "POST", body: JSON.stringify(data) }),
  getCriteria: () => apiFetch("/api/v1/compliance/criteria"),
  getClassifications: () => apiFetch("/api/v1/compliance/classifications"),
  getAgents: () => apiFetch("/api/v1/agents/"),
  runDPIA: (activity) =>
    apiFetch("/api/v1/agents/dpia/run", { method: "POST", body: JSON.stringify({ organisation_id: "dashboard", processing_activity: activity }) }),
  runFRIA: (system) =>
    apiFetch("/api/v1/agents/fria/run", { method: "POST", body: JSON.stringify({ organisation_id: "dashboard", ai_system: system }) }),
  runRegulatoryScan: () =>
    apiFetch("/api/v1/agents/regulatory/scan", { method: "POST" }),
  getPolicies: () => apiFetch("/api/v1/policies/"),
  evaluatePolicies: (context) =>
    apiFetch("/api/v1/policies/evaluate", { method: "POST", body: JSON.stringify({ context }) }),
};
