/**
 * JuraRegel API Client
 *
 * Connects to the JuraRegel REST API.
 * For static export, uses mock data when API is unavailable.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "";

// ─── Types ───────────────────────────────────────────────────

export interface Template {
  id: string;
  document: string;
  wettelijke_basis: string;
  model_versie: string;
  section_count: number;
  has_checkboxes: boolean;
  has_scoring: boolean;
  category: string;
}

export interface ComplianceScore {
  score: number;
  classification: string;
  classification_label: string;
  classification_color: string;
  criteria: Array<{
    name: string;
    weight: number;
    raw_score: number;
    weighted_score: number;
    details: string;
  }>;
  recommendations: string[];
  calculated_at: string;
}

export interface AgentResult {
  agent: string;
  status: string;
  output: Record<string, unknown>;
  citations: Array<{ source: string; passage: string }>;
  confidence: number;
  recommendations: string[];
  execution_time_ms: number;
  trace: Array<{ step: string; status: string; [key: string]: unknown }>;
}

export interface PolicySummary {
  total_policies: number;
  compliant: number;
  non_compliant: number;
  compliance_rate: number;
  violations: Array<{
    policy_id: string;
    article: string;
    message: string;
    severity: string;
    remediation: string;
    citation: string;
  }>;
  critical_violations: number;
  high_violations: number;
}

// ─── API Client ──────────────────────────────────────────────

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  if (!API_URL) throw new Error("API_URL not configured");

  const resp = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!resp.ok) throw new Error(`API error: ${resp.status}`);
  return resp.json();
}

// ─── API Methods ─────────────────────────────────────────────

export const api = {
  // Templates
  getTemplates: () => apiFetch<Template[]>("/api/v1/templates/"),
  generateTemplate: (id: string, params: Record<string, unknown>) =>
    apiFetch(`/api/v1/templates/${id}/generate`, {
      method: "POST",
      body: JSON.stringify({ organisation: "Dashboard", parameters: params }),
    }),

  // Compliance
  getScore: (data: Record<string, unknown>) =>
    apiFetch<ComplianceScore>("/api/v1/compliance/score", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  getCriteria: () => apiFetch("/api/v1/compliance/criteria"),
  getClassifications: () => apiFetch("/api/v1/compliance/classifications"),

  // Agents
  getAgents: () => apiFetch("/api/v1/agents/"),
  runDPIA: (activity: Record<string, unknown>) =>
    apiFetch<AgentResult>("/api/v1/agents/dpia/run", {
      method: "POST",
      body: JSON.stringify({ organisation_id: "dashboard", processing_activity: activity }),
    }),
  runFRIA: (system: Record<string, unknown>) =>
    apiFetch<AgentResult>("/api/v1/agents/fria/run", {
      method: "POST",
      body: JSON.stringify({ organisation_id: "dashboard", ai_system: system }),
    }),
  runRegulatoryScan: () =>
    apiFetch<AgentResult>("/api/v1/agents/regulatory/scan", { method: "POST" }),

  // Policies
  getPolicies: () => apiFetch("/api/v1/policies/"),
  evaluatePolicies: (context: Record<string, unknown>) =>
    apiFetch<PolicySummary>("/api/v1/policies/evaluate", {
      method: "POST",
      body: JSON.stringify({ context }),
    }),
};
