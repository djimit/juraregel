export default function ArchitecturePage() {
  const layers = [
    {
      name: "Presentatie",
      color: "bg-blue-50 border-blue-500",
      components: ["Dashboard", "Assessment Workspace", "Regulatory Monitor", "Audit Console"],
    },
    {
      name: "API Gateway",
      color: "bg-green-50 border-green-500",
      components: ["REST (OpenAPI 3.1)", "GraphQL", "OAuth2 + mTLS", "Rate Limiting"],
    },
    {
      name: "Core Services",
      color: "bg-yellow-50 border-yellow-500",
      components: ["Template Service", "Assessment Engine", "Evidence Service", "Workflow Engine", "Compliance Scoring"],
    },
    {
      name: "AI / LLM",
      color: "bg-purple-50 border-purple-500",
      components: ["RAG Pipeline", "Knowledge Graph (NMF)", "Legal Reasoning", "Hallucination Detection"],
    },
    {
      name: "Data",
      color: "bg-red-50 border-red-500",
      components: ["PostgreSQL + RLS", "Qdrant (Vectors)", "Redis (Cache)", "Immutable Audit Log"],
    },
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold text-[#1a365d] mb-2">Architectuur</h1>
      <p className="text-gray-500 mb-8">Living Compliance Engine — van presentatie tot data-laag</p>

      {/* Architecture layers */}
      <div className="space-y-4 mb-8">
        {layers.map((layer) => (
          <div key={layer.name} className={`${layer.color} border-l-4 rounded-xl p-5`}>
            <h3 className="font-bold text-[#1a365d] mb-3">{layer.name}</h3>
            <div className="flex flex-wrap gap-2">
              {layer.components.map((c) => (
                <span key={c} className="bg-white px-4 py-2 rounded-lg text-sm font-medium text-gray-700 shadow-sm">
                  {c}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Tech stack */}
      <h2 className="text-xl font-bold text-[#1a365d] mb-4">Tech Stack</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        [
          { name: "Backend", tech: "Python + FastAPI", desc: "Async REST API" },
          { name: "Database", tech: "PostgreSQL 16", desc: "Multi-tenant + RLS" },
          { name: "Vector Store", tech: "Qdrant", desc: "Hybrid search" },
          { name: "Auth", tech: "Keycloak", desc: "OAuth2 / OIDC" },
          { name: "Frontend", tech: "Next.js 15", desc: "React + Tailwind" },
          { name: "LLM", tech: "Claude", desc: "Juridische reasoning" },
        ].map((item) => (
          <div key={item.name} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">{item.name}</p>
            <p className="text-lg font-bold text-[#1a365d]">{item.tech}</p>
            <p className="text-sm text-gray-500 mt-1">{item.desc}</p>
          </div>
        ))}
      </div>

      {/* Data flow */}
      <h2 className="text-xl font-bold text-[#1a365d] mb-4">Data Flow</h2>
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <pre className="text-sm text-gray-700 font-mono leading-relaxed">{`Wetgeving (EUR-Lex, Staatsblad, EDPB)
    │
    ▼
Document Ingestion → Parse → Chunk → Embed → Store (Qdrant)
                                    │
                                    ▼
Query → Hybrid Search (BM25 + Dense) → Re-rank → Context
                                    │
                                    ▼
LLM Generation (Claude) → Citation Verify → Halluc. Check
                                    │
                                    ▼
Response + Audit Trail (immutable)`}</pre>
      </div>
    </div>
  );
}
