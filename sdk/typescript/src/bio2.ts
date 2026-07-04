import { JuraregelClient } from "./client.js";
import type { CalculateRequest, CalculateResponse, HealthResponse } from "./types.js";

export class UBio2Client extends JuraregelClient {
  constructor(baseUrl: string = "http://127.0.0.1:8494") {
    super(baseUrl);
  }

  async health(): Promise<HealthResponse> {
    return super.health();
  }

  async calculate(request: CalculateRequest): Promise<CalculateResponse> {
    return super.calculate("bio2", request);
  }
}
