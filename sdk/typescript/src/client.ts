// JuraRegel SDK — Base HTTP client

export class JuraregelClient {
  constructor(private baseUrl: string) {}

  async health(): Promise<any> {
    const r = await fetch(`${this.baseUrl}/v1/health`);
    return r.json();
  }

  protected async calculateDomain<T>(domain: string, request: unknown): Promise<T> {
    const r = await fetch(`${this.baseUrl}/v1/${domain}/calculate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    if (!r.ok) throw new Error(`API error: ${r.status} ${r.statusText}`);
    return r.json() as Promise<T>;
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
