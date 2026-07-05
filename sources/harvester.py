#!/usr/bin/env python3
"""BWB Harvester - downloads and tracks Dutch legislation from wetten.overheid.nl."""
import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).parent.parent
STATE_FILE = REPO_ROOT / ".data" / "harvester-state.json"
BWB_BASE = "https://wetten.overheid.nl"


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"last_check": None, "documents": {}}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def fetch_bwb_list():
    """Fetch list of available laws from BWB."""
    try:
        url = f"{BWB_BASE}/api/v1/wetten"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def fetch_wet_metadata(bwb_id):
    """Fetch metadata for a specific law."""
    try:
        url = f"{BWB_BASE}/api/v1/wetten/{bwb_id}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e), "bwb_id": bwb_id}


def check_for_updates():
    """Check BWB for new or updated documents."""
    state = load_state()
    current_time = datetime.now(timezone.utc).isoformat()
    
    bwb_list = fetch_bwb_list()
    if "error" in bwb_list:
        return {"status": "error", "error": bwb_list["error"], "updates": []}
    
    updates = []
    documents = bwb_list.get("wetten", [])
    
    for doc in documents[:10]:  # Limit to first 10 for rate limiting
        bwb_id = doc.get("bwbId", doc.get("bwb_id", ""))
        if not bwb_id:
            continue
        
        last_hash = state.get("documents", {}).get(bwb_id, {}).get("hash")
        current_hash = str(hash(json.dumps(doc, sort_keys=True)))
        
        if last_hash != current_hash:
            updates.append({
                "bwb_id": bwb_id,
                "titel": doc.get("titel", doc.get("title", "")),
                "status": "new" if bwb_id not in state.get("documents", {}) else "updated",
            })
            state.setdefault("documents", {})[bwb_id] = {
                "hash": current_hash,
                "last_seen": current_time,
                "titel": doc.get("titel", doc.get("title", "")),
            }
    
    state["last_check"] = current_time
    save_state(state)
    
    return {
        "status": "ok",
        "checked": len(documents),
        "updates": updates,
        "timestamp": current_time,
    }


def health_check():
    """Check if BWB endpoint is reachable."""
    try:
        url = f"{BWB_BASE}/api/v1/wetten"
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return {"source": "BWB", "status": "ok", "http_code": resp.status}
    except Exception as e:
        return {"source": "BWB", "status": "error", "error": str(e)}


if __name__ == "__main__":
    import sys
    if "--health" in sys.argv:
        print(json.dumps(health_check(), indent=2, ensure_ascii=False))
    elif "--check" in sys.argv:
        print(json.dumps(check_for_updates(), indent=2, ensure_ascii=False))
    elif "--state" in sys.argv:
        print(json.dumps(load_state(), indent=2, ensure_ascii=False))
    else:
        print("Usage: python3 sources/harvester.py [--health|--check|--state]")
