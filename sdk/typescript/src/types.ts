// JuraRegel SDK — Shared types

export interface CalculateRequest {
  calculationDate: string;
  zaak: ZaakInput;
  partij: PartijInput;
  zaakIdentificatie?: string;
  tariefjaar?: number;
}

export interface ZaakInput {
  rechtsgebied: string;
  zaakstroom: string;
  procedureType: string;
  vorderingWaarde: number | string;
  bijzondereCategorie: string;
}

export interface PartijInput {
  rol: string;
  partijType: string;
  onvermogend: boolean;
  verweerStatus: string;
}

export interface CalculateResponse {
  calculationId: string;
  ruleSetVersion: string;
  domain: string;
  result: {
    griffierecht: { amount: number | null; currency: string };
    category: string;
    verschuldigdDoor: string | null;
    manualReviewRequired: boolean;
  };
  explanation: {
    summary: string;
    reasoningSteps: string[];
    appliedRules: string[];
    sourceRefs: SourceRef[];
  };
  warnings: string[];
  juridischeContext: JuridischeContext | null;
  audit: {
    inputHash: string;
    rulesetHash: string;
    timestamp: string;
  };
}

export interface SourceRef {
  type?: string;
  title: string;
  section?: string;
  url?: string;
}

export interface JuridischeContext {
  wet: string;
  wetBwbrId: string;
  wetVersieLaatstGecheckt: string;
  tariefVersie: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  domain: string;
  rulesetVersions: Array<{
    version: string;
    validFrom: string;
    validUntil: string;
    ruleCount: number;
    scenarioCount: number;
    hasAcceptatie: boolean;
  }>;
}
