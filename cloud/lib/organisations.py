"""JuraRegel Cloud — Organisation & API Key Management.

Multi-tenant architectuur:
- Elke organisatie heeft een unieke ID, API keys, en usage limits
- API keys worden gehashed opgeslagen (SHA-256)
- Usage tracking per organisatie per maand
- Rate limiting per API key
"""

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import json


@dataclass
class Organisation:
    org_id: str
    name: str
    contact_email: str
    plan: str = "community"  # community, pro, enterprise
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    api_keys: list[dict] = field(default_factory=list)
    usage: dict = field(
        default_factory=dict
    )  # { "2026-07": { "requests": 0, "endpoints": {} } }
    enabled: bool = True

    # Plan limits
    PLAN_LIMITS = {
        "community": {
            "requests_per_month": 1000,
            "max_api_keys": 1,
            "max_frameworks": 3,
        },
        "pro": {"requests_per_month": 50000, "max_api_keys": 5, "max_frameworks": 10},
        "enterprise": {
            "requests_per_month": 1_000_000,
            "max_api_keys": 50,
            "max_frameworks": 100,
        },
    }

    @property
    def limits(self) -> dict:
        return self.PLAN_LIMITS.get(self.plan, self.PLAN_LIMITS["community"])

    @property
    def current_month_usage(self) -> int:
        month = date.today().strftime("%Y-%m")
        return self.usage.get(month, {}).get("requests", 0)

    @property
    def is_within_limits(self) -> bool:
        return self.current_month_usage < self.limits["requests_per_month"]

    def can_add_api_key(self) -> bool:
        return len(self.api_keys) < self.limits["max_api_keys"]

    def generate_api_key(self, name: str = "default") -> str:
        """Genereert een API key. De plaintext key wordt één keer geretourneerd."""
        if not self.can_add_api_key():
            raise ValueError(
                f"Max API keys ({self.limits['max_api_keys']}) reached for plan {self.plan}"
            )

        plaintext = f"jrg_{secrets.token_urlsafe(32)}"
        hashed = hashlib.sha256(plaintext.encode()).hexdigest()

        key_entry = {
            "name": name,
            "key_hash": hashed,
            "created_at": datetime.now().isoformat(),
            "last_used": None,
            "enabled": True,
        }
        self.api_keys.append(key_entry)
        return plaintext

    def validate_api_key(self, plaintext_key: str) -> bool:
        """Valideert een API key tegen de hashed versies."""
        hashed = hashlib.sha256(plaintext_key.encode()).hexdigest()
        for key in self.api_keys:
            if key["key_hash"] == hashed and key["enabled"]:
                key["last_used"] = datetime.now().isoformat()
                return True
        return False

    def track_request(self, endpoint: str):
        """Track een API request voor usage monitoring."""
        month = date.today().strftime("%Y-%m")
        if month not in self.usage:
            self.usage[month] = {"requests": 0, "endpoints": {}}
        self.usage[month]["requests"] += 1
        self.usage[month]["endpoints"][endpoint] = (
            self.usage[month]["endpoints"].get(endpoint, 0) + 1
        )

    def to_dict(self) -> dict:
        return {
            "org_id": self.org_id,
            "name": self.name,
            "contact_email": self.contact_email,
            "plan": self.plan,
            "created_at": self.created_at,
            "api_keys": [
                {k: v for k, v in key.items() if k != "key_hash"}
                for key in self.api_keys
            ],
            "usage": self.usage,
            "enabled": self.enabled,
            "limits": self.limits,
        }


class OrganisationStore:
    """File-based organisatie store (voor PoC — productie gebruikt PostgreSQL)."""

    def __init__(self, store_path: Path | None = None):
        self.store_path = (
            store_path or Path(__file__).parent.parent / "data" / "organisations.json"
        )
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        self._organisations: dict[str, Organisation] = {}
        self._load()

    def _load(self):
        if self.store_path.exists():
            with open(self.store_path) as f:
                data = json.load(f)
            for org_id, org_data in data.items():
                # Filter out non-field keys (limits, current_month_usage are properties)
                valid_fields = {
                    f.name for f in Organisation.__dataclass_fields__.values()
                }
                filtered = {k: v for k, v in org_data.items() if k in valid_fields}
                self._organisations[org_id] = Organisation(**filtered)

    def _save(self):
        data = {org_id: org.to_dict() for org_id, org in self._organisations.items()}
        with open(self.store_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def create(
        self, name: str, contact_email: str, plan: str = "community"
    ) -> tuple[Organisation, str]:
        """Maak een organisatie aan. Retourneert (org, api_key)."""
        org_id = f"org_{secrets.token_urlsafe(8)}"
        org = Organisation(
            org_id=org_id, name=name, contact_email=contact_email, plan=plan
        )
        api_key = org.generate_api_key("default")
        self._organisations[org_id] = org
        self._save()
        return org, api_key

    def get(self, org_id: str) -> Optional[Organisation]:
        return self._organisations.get(org_id)

    def get_by_api_key(self, api_key: str) -> Optional[Organisation]:
        """Zoekt organisatie op basis van API key."""
        for org in self._organisations.values():
            if org.validate_api_key(api_key):
                return org
        return None

    def list_all(self) -> list[Organisation]:
        return list(self._organisations.values())

    def update(self, org: Organisation):
        self._organisations[org.org_id] = org
        self._save()

    def delete(self, org_id: str):
        self._organisations.pop(org_id, None)
        self._save()


# ─── Singleton store ─────────────────────────────────────────
_store: Optional[OrganisationStore] = None


def get_store() -> OrganisationStore:
    global _store
    if _store is None:
        _store = OrganisationStore()
    return _store
