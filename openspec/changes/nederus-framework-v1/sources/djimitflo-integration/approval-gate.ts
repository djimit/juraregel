/**
 * NEDERUS Approval Gate for Djimitflo
 *
 * Enforces approval rules: high-severity controls require 2 approvers.
 * Part of NEDERUS × Djimitflo integration (Phase 4).
 *
 * Location in Djimitflo: src/compliance/approval-gate.ts
 */

import { ComplianceTask } from "./task-generator";

export function canApprove(task: ComplianceTask, approverId: string): boolean {
  if (task.status !== "evidence_submitted" && task.status !== "review") {
    return false;
  }
  if (task.approvers.includes(approverId)) {
    return false; // already approved
  }
  return true;
}

export function submitApproval(
  task: ComplianceTask,
  approverId: string
): ComplianceTask {
  if (!canApprove(task, approverId)) {
    throw new Error(`Cannot approve task ${task.id}: invalid state or duplicate`);
  }

  const approvers = [...task.approvers, approverId];
  const fullyApproved = approvers.length >= task.max_approvers;

  return {
    ...task,
    approvers,
    status: fullyApproved ? "approved" : "review",
  };
}

export function isFullyApproved(task: ComplianceTask): boolean {
  return task.approvers.length >= task.max_approvers;
}
