import { JuraregelClient } from "./client.js";
import type { CalculateRequest, CalculateResponse, HealthResponse } from "./types.js";

export class UoverheidsstandaardenClient extends JuraregelClient {
  constructor(baseUrl: string = "http://127.0.0.1:8496") {
    super(baseUrl);
  }

  async health(): Promise<HealthResponse> {
    return super.health();
  }

  async calculate(request: CalculateRequest): Promise<CalculateResponse> {
    return super.calculate("overheidsstandaarden", request);
  }
}
