/**
 * NEDERUS Controls Loader for Djimitflo
 *
 * Reads controls.yaml from git submodule or local path.
 * Part of NEDERUS × Djimitflo integration (Phase 4).
 *
 * Location in Djimitflo: src/compliance/controls-loader.ts
 */

import { readFileSync } from "fs";
import { parse as parseYaml } from "yaml";

export interface FrameworkRef {
  function?: string;
  reference: string;
  relation: "equivalent" | "partial" | "gap";
}

export interface Control {
  id: string;
  title: string;
  description: string;
  severity: "low" | "medium" | "high" | "critical";
  status?: "active" | "deprecated";
  frameworks: {
    nist_ai_rmf: FrameworkRef;
    eu_ai_act: FrameworkRef;
    bio2: FrameworkRef;
    nis2: FrameworkRef;
    nora: FrameworkRef;
  };
  evidence_required: string[];
  implementation_guidance: string;
}

export interface ControlCatalog {
  version: string;
  last_updated: string;
  frameworks: Record<string, string>;
  controls: Control[];
}

const DEFAULT_PATH = "./src/compliance/data/controls.yaml";

export function loadControls(path: string = DEFAULT_PATH): Control[] {
  const raw = readFileSync(path, "utf8");
  const doc = parseYaml(raw) as ControlCatalog;
  return doc.controls.filter((c) => c.status !== "deprecated");
}

export function getControlById(id: string, path?: string): Control | undefined {
  return loadControls(path).find((c) => c.id === id);
}
