#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

COLLECTION = "juraregel-rules"
VECTOR_SIZE = 1536
STORE_PATH = ".qdrant"

def get_repo_root():
    return Path(__file__).parent.parent

def load_jkb_index():
    path = get_repo_root() / "knowledge-base" / "jkb-index.json"
    return json.loads(path.read_text())

def default_embed_fn(texts):
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", "sk-placeholder"),
        base_url=os.environ.get("OPENAI_API_BASE", "http://192.168.1.28:4000/v1"),
    )
    resp = client.embeddings.create(
        model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small"),
        input=texts,
    )
    return [d.embedding for d in resp.data]

def init_qdrant(path=STORE_PATH):
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
    client = QdrantClient(path=path)
    try:
        client.get_collection(COLLECTION)
    except Exception:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )
    return client

def index_rules(client, jkb_index, embed_fn=None):
    from qdrant_client.models import PointStruct
    embed_fn = embed_fn or default_embed_fn
    texts = [e["embedding_text"] for e in jkb_index]
    vectors = embed_fn(texts)
    points = []
    for i, (entry, vector) in enumerate(zip(jkb_index, vectors)):
        points.append(PointStruct(
            id=i, vector=vector,
            payload={
                "rule_id": entry["rule_id"], "domain": entry["domain"],
                "version": entry["version"], "name": entry["name"],
                "nl_text": entry["nl_text"], "source_refs": entry["source_refs"],
                "valid_from": entry["valid_from"], "valid_until": entry["valid_until"],
            },
        ))
    client.upsert(collection_name=COLLECTION, points=points)
    return len(points)

def search(client, query, embed_fn=None, domain=None, limit=10):
    from qdrant_client.models import Filter, FieldCondition, MatchValue
    embed_fn = embed_fn or default_embed_fn
    vector = embed_fn([query])[0]
    qf = Filter(must=[FieldCondition(key="domain", match=MatchValue(value=domain))]) if domain else None
    results = client.search(collection_name=COLLECTION, query_vector=vector, query_filter=qf, limit=limit)
    return [{"rule_id": r.payload["rule_id"], "domain": r.payload["domain"], "name": r.payload["name"], "nl_text": r.payload["nl_text"][:200], "score": round(r.score, 4)} for r in results]

def check_coverage(expected_count):
    from qdrant_client import QdrantClient
    client = QdrantClient(path=STORE_PATH)
    info = client.get_collection(COLLECTION)
    indexed = info.points_count
    return {"indexed": indexed, "expected": expected_count, "complete": indexed == expected_count}

if __name__ == "__main__":
    repo_root = get_repo_root()
    jkb_index = load_jkb_index()
    if len(sys.argv) < 2:
        print("Usage: python3 tools/jkb-vectorstore.py [index|search|--check-coverage]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "index":
        client = init_qdrant(str(repo_root / STORE_PATH))
        count = index_rules(client, jkb_index)
        print(f"Indexed {count} rules into Qdrant ({STORE_PATH}/)")
    elif cmd == "search":
        query = " ".join(sys.argv[2:])
        domain = None
        if "--domain" in sys.argv:
            idx = sys.argv.index("--domain")
            domain = sys.argv[idx + 1]
        client = init_qdrant(str(repo_root / STORE_PATH))
        results = search(client, query.strip(), domain=domain)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif cmd == "--check-coverage":
        result = check_coverage(len(jkb_index))
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["complete"] else 1)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
