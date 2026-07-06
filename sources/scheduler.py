"""
Connector Scheduler — runs all connectors in sequence with health checks.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sources.bwb_connector import BWBConnector
from sources.cvdr_sru_connector import CVDRSRUConnector
from sources.eurlex_connector import EURLexConnector
from sources.plooi_connector import PLOOIConnector
from sources.rechtspraak_connector import RechtspraakConnector
from sources.sttr_rtr_connector import STTRRTRConnector
from sources.tooi_roo_connector import TOOIROOConnector
from sources.upl_connector import UPLConnector
from sources.woo_diwoo_connector import WooDiWooConnector

SOURCE_HEALTH_STATUSES = {"ok", "degraded", "deprecated", "unsupported_method", "error"}

ALL_CONNECTORS = [
    BWBConnector,
    EURLexConnector,
    PLOOIConnector,
    RechtspraakConnector,
    UPLConnector,
    TOOIROOConnector,
    CVDRSRUConnector,
    WooDiWooConnector,
    STTRRTRConnector,
]

def run_health_checks() -> list[dict]:
    """Run health checks for all connectors."""
    results = []
    for cls in ALL_CONNECTORS:
        try:
            c = cls()
            results.append(c.health_check())
        except Exception as e:
            results.append({"source": cls.__name__, "status": "error", "error": str(e)})
    return results

def run_ingest() -> dict:
    """Run list_sources for all connectors."""
    results = {}
    for cls in ALL_CONNECTORS:
        try:
            c = cls()
            name = cls.__name__
            sources = c.list_sources()
            results[name] = {"count": len(sources), "sources": sources[:3]}
        except Exception as e:
            results[cls.__name__] = {"error": str(e)}
    return results

def run_live_smoke() -> list[dict]:
    """Run optional live smoke checks for connectors that expose them."""
    results = []
    for cls in (CVDRSRUConnector, WooDiWooConnector, STTRRTRConnector):
        try:
            connector = cls()
            results.append(connector.live_smoke())
        except Exception as e:
            results.append({"source": cls.__name__, "status": "error", "error": str(e)})
    return results

if __name__ == "__main__":
    import sys
    if "--health" in sys.argv:
        print(json.dumps(run_health_checks(), indent=2))
    elif "--ingest" in sys.argv:
        print(json.dumps(run_ingest(), indent=2))
    elif "--live-smoke" in sys.argv:
        print(json.dumps(run_live_smoke(), indent=2))
    else:
        print("Usage: python3 sources/scheduler.py [--health|--ingest|--live-smoke]")
