#!/usr/bin/env python3
import json, sqlite3, sys
from pathlib import Path

DB_PATH = ".keyword.db"

def get_repo_root():
    return Path(__file__).parent.parent

def load_jkb_index():
    path = get_repo_root() / "knowledge-base" / "jkb-index.json"
    return json.loads(path.read_text())

def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS rules USING fts5("
                 "rule_id UNINDEXED, domain UNINDEXED, name, nl_text, "
                 "source_titles, version UNINDEXED, tokenize='unicode61')")
    return conn

def index_rules(conn, jkb_index):
    conn.execute("DELETE FROM rules")
    rows = []
    for e in jkb_index:
        source_titles = " ".join(r.get("title", "") for r in e.get("source_refs", []))
        rows.append((e["rule_id"], e["domain"], e["name"], e["nl_text"], source_titles, e["version"]))
    conn.executemany("INSERT INTO rules (rule_id, domain, name, nl_text, source_titles, version) VALUES (?,?,?,?,?,?)", rows)
    conn.commit()
    return len(rows)

def search(conn, query, domain=None, limit=20):
    terms = query.replace('"', '').strip().split()
    fts_query = " ".join('"' + t + '"' for t in terms if t)
    if domain:
        sql = "SELECT rule_id, domain, name, nl_text FROM rules WHERE rules MATCH ? AND domain = ? ORDER BY rank LIMIT ?"
        rows = conn.execute(sql, (fts_query, domain, limit)).fetchall()
    else:
        sql = "SELECT rule_id, domain, name, nl_text FROM rules WHERE rules MATCH ? ORDER BY rank LIMIT ?"
        rows = conn.execute(sql, (fts_query, limit)).fetchall()
    return [{"rule_id": r[0], "domain": r[1], "name": r[2], "nl_text": r[3][:200]} for r in rows]

def check_coverage(expected_count):
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
    return {"indexed": count, "expected": expected_count, "complete": count == expected_count}

def parse_args(argv):
    domain = None
    if "--domain" in argv:
        idx = argv.index("--domain")
        domain = argv[idx + 1] if idx + 1 < len(argv) else None
        argv = argv[:idx] + argv[idx+2:]
    query = " ".join(argv[2:]).strip()
    return query, domain

if __name__ == "__main__":
    repo_root = get_repo_root()
    jkb_index = load_jkb_index()
    if len(sys.argv) < 2:
        print("Usage: python3 tools/jkb-keyword.py [index|search|--check-coverage]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "index":
        conn = init_db(str(repo_root / DB_PATH))
        count = index_rules(conn, jkb_index)
        print(f"Indexed {count} rules into SQLite FTS5 ({DB_PATH})")
        conn.close()
    elif cmd == "search":
        query, domain = parse_args(sys.argv)
        conn = init_db(str(repo_root / DB_PATH))
        results = search(conn, query, domain=domain)
        print(json.dumps(results, indent=2, ensure_ascii=False))
        conn.close()
    elif cmd == "--check-coverage":
        result = check_coverage(len(jkb_index))
        print(json.dumps(result, indent=2))
        sys.exit(0 if result["complete"] else 1)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
