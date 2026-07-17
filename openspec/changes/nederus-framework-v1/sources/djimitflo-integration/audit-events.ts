/**
 * NEDERUS Compliance Audit Events for Djimitflo
 *
 * Extends Djimitflo's audit trail with compliance-specific events.
 * Part of NEDERUS × Djimitflo integration (Phase 4).
 *
 * Location in Djimitflo: src/compliance/audit-events.ts
 */

export interface ComplianceAuditEvent {
  type: "compliance-evaluated";
  control_id: string;
  control_title: string;
  result: "passed" | "failed" | "pending";
  evidence_refs: string[];
  evaluator: string;
  timestamp: string;
  framework_refs: {
    nist_ai_rmf?: string;
    eu_ai_act?: string;
    bio2?: string;
    nis2?: string;
    nora?: string;
  };
}

export function createComplianceEvent(params: {
  control_id: string;
  control_title: string;
  result: "passed" | "failed" | "pending";
  evidence_refs: string[];
  evaluator: string;
  framework_refs?: ComplianceAuditEvent["framework_refs"];
}): ComplianceAuditEvent {
  return {
    type: "compliance-evaluated",
    control_id: params.control_id,
    control_title: params.control_title,
    result: params.result,
    evidence_refs: params.evidence_refs,
    evaluator: params.evaluator,
    timestamp: new Date().toISOString(),
    framework_refs: params.framework_refs ?? {},
  };
}
