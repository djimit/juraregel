/**
 * NEDERUS Compliance Task Generator for Djimitflo
 *
 * Converts NEDERUS Control[] into Djimitflo Task[].
 * Part of NEDERUS × Djimitflo integration (Phase 4).
 *
 * Location in Djimitflo: src/compliance/task-generator.ts
 */

import { loadControls, Control } from "./controls-loader";

export interface ComplianceTask {
  id: string;
  type: "compliance-check";
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  control: Control;
  status: "pending" | "evidence_submitted" | "review" | "approved" | "rejected";
  evidence_required: string[];
  evidence_provided: string[];
  approvers: string[];
  max_approvers: number;
  created_at: string;
}

function mapSeverityToApprovers(severity: string): number {
  switch (severity) {
    case "critical":
    case "high":
      return 2;
    default:
      return 1;
  }
}

export function generateComplianceTasks(
  controlsPath?: string
): ComplianceTask[] {
  const controls = loadControls(controlsPath);

  return controls.map((control) => ({
    id: `COMPLIANCE-${control.id}`,
    type: "compliance-check" as const,
    title: `[${control.severity.toUpperCase()}] ${control.title}`,
    severity: control.severity,
    control,
    status: "pending" as const,
    evidence_required: [...control.evidence_required],
    evidence_provided: [],
    approvers: [],
    max_approvers: mapSeverityToApprovers(control.severity),
    created_at: new Date().toISOString(),
  }));
}
