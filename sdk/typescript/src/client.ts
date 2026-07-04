// JuraRegel SDK — Base HTTP client

export class JuraregelClient {
  constructor(private baseUrl: string) {}

  async health(): Promise<any> {
    const r = await fetch(`${this.baseUrl}/v1/health`);
    return r.json();
  }

  async calculate(domain: string, request: any): Promise<any> {
    const r = await fetch(`${this.baseUrl}/v1/${domain}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!r.ok) throw new Error(`API error: ${r.status} ${r.statusText}`);
    return r.json();
  }

  async getAudit(calculationId: string): Promise<any> {
    const r = await fetch(`${this.baseUrl}/v1/audit/${calculationId}`);
    return r.json();
  }

  async getVersions(domain: string): Promise<any> {
    const r = await fetch(`${this.baseUrl}/v1/${domain}/versions`);
    return r.json();
  }
}
