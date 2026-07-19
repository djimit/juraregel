"""JuraRegel Regel-Automatische Updates — Scraper voor wet- en regelgeving.

Monitort wijzigingen in:
- wetten.overheid.nl (Nederlandse wetgeving)
- eur-lex.europa.eu (EU-verordeningen)
- officielebekendmakingen.nl (Staatsbladen)

Wanneer een wijziging wordt gedetecteerd:
1. Nieuwe regel wordt toegevoegd of bestaande regel bijgewerkt
2. Versie wordt opgeslagen in CHANGELOG.md
3. Notificatie wordt verstuurd (webhook/email)
"""

import hashlib
import json
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Optional

# ─── Bron configuratie ─────────────────────────────────────

SOURCES = {
    "wetten_overheid": {
        "name": "Wetten.overheid.nl",
        "base_url": "https://wetten.overheid.nl",
        "type": "nl_wetgeving",
        "check_interval_hours": 24,
        "frameworks": ["wdo", "avg-gdpr", "eu-ai-act"],
    },
    "eur_lex": {
        "name": "EUR-Lex",
        "base_url": "https://eur-lex.europa.eu",
        "type": "eu_verordening",
        "check_interval_hours": 24,
        "frameworks": ["eu-ai-act", "eidas", "avg-gdpr", "nis2"],
    },
    "officiele_bekendmakingen": {
        "name": "Officiële Bekendmakingen",
        "base_url": "https://zoek.officielebekendmakingen.nl",
        "type": "nl_publicatie",
        "check_interval_hours": 12,
        "frameworks": ["wdo", "bio2-informatiebeveiliging"],
    },
}

# ─── Checksum tracking ─────────────────────────────────────


def compute_checksum(content: str) -> str:
    """Bereken SHA-256 checksum van content."""
    return hashlib.sha256(content.encode()).hexdigest()


class RuleUpdater:
    """Monitort en update regels automatisch."""

    def __init__(self, state_path: Path | None = None):
        self.state_path = state_path or Path(__file__).parent / "update_state.json"
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_path.exists():
            with open(self.state_path) as f:
                return json.load(f)
        return {"last_checks": {}, "checksums": {}, "pending_updates": []}

    def _save_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state, f, indent=2, default=str)

    def check_source(self, source_id: str) -> dict:
        """Check een bron op wijzigingen. Geeft update-status terug."""
        source = SOURCES.get(source_id)
        if not source:
            return {"error": f"Unknown source: {source_id}"}

        last_check = self.state["last_checks"].get(source_id, "Never")
        checksum = self.state["checksums"].get(source_id, "")

        # In productie: fetch actual content and compare checksum
        # Voor PoC: simulatie
        return {
            "source": source["name"],
            "last_check": last_check,
            "current_checksum": checksum,
            "status": "up_to_date",
            "frameworks_affected": source["frameworks"],
            "next_check": "Binnen 24 uur",
        }

    def check_all(self) -> list[dict]:
        """Check alle bronnen op wijzigingen."""
        results = []
        for source_id in SOURCES:
            results.append(self.check_source(source_id))
        return results

    def apply_update(self, framework: str, rule_id: str, new_content: str) -> dict:
        """Pas een regel-wijziging toe."""
        update = {
            "framework": framework,
            "rule_id": rule_id,
            "applied_at": datetime.now().isoformat(),
            "checksum": compute_checksum(new_content),
            "previous_checksum": self.state["checksums"].get(
                f"{framework}:{rule_id}", ""
            ),
        }
        self.state["checksums"][f"{framework}:{rule_id}"] = update["checksum"]
        self.state["pending_updates"].append(update)
        self._save_state()
        return update

    def get_pending_updates(self) -> list[dict]:
        """Geef alle openstaande updates."""
        return self.state.get("pending_updates", [])

    def generate_changelog_entry(self, update: dict) -> str:
        """Genereer een changelog-regel voor een update."""
        return f"- [{update['applied_at'][:10]}] {update['framework']}/{update['rule_id']}: automatische update"


# ─── CLI interface ─────────────────────────────────────────


def main():
    updater = RuleUpdater()
    print("JuraRegel Regel-Automatische Updates")
    print("=" * 50)

    results = updater.check_all()
    for r in results:
        print(f"  {r['source']}: {r['status']} ({', '.join(r['frameworks_affected'])})")

    pending = updater.get_pending_updates()
    print(f"\nOpenstaande updates: {len(pending)}")


if __name__ == "__main__":
    main()
