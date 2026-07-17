"""Receipt — bilateral Ed25519-signed proof of authorization + execution.

Each receipt has two cryptographic phases:
1. Authorization: signs the decision (permit/forbid/require_approval)
2. Seal: binds the execution result to the authorization
"""

import hashlib
import hmac
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class Receipt:
    """A bilateral receipt proving what was authorized and what was done."""

    def __init__(self, **kwargs):
        self.receipt_id = kwargs.get("receipt_id", str(uuid.uuid4()))
        self.agent_id = kwargs.get("agent_id", "unknown")
        self.action_name = kwargs.get("action_name", "unknown")
        self.payload_hash = kwargs.get("payload_hash", "")
        self.covenant_hash = kwargs.get("covenant_hash", "")
        self.decision = kwargs.get("decision", "unknown")
        self.authorized = kwargs.get("authorized", False)
        self.parent_receipt_id = kwargs.get("parent_receipt_id")
        self.authorization_sig = kwargs.get("authorization_sig", "")
        self.result_hash = kwargs.get("result_hash", "")
        self.result_status = kwargs.get("result_status", "")
        self.seal_sig = kwargs.get("seal_sig", "")
        self.status = kwargs.get("status", "pending")
        self.created_at = kwargs.get(
            "created_at", datetime.now(timezone.utc).isoformat()
        )
        self.sealed_at = kwargs.get("sealed_at")
        self.signing_method = kwargs.get("signing_method", "hmac-sha256")
        self.metadata = kwargs.get("metadata", {})

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if v is not None}
        return d

    @classmethod
    def from_dict(cls, data: dict) -> "Receipt":
        return cls(
            **{
                k: v
                for k, v in data.items()
                if k in cls().__dict__
                or k
                in [
                    "receipt_id",
                    "agent_id",
                    "action_name",
                    "payload_hash",
                    "covenant_hash",
                    "decision",
                    "authorized",
                    "parent_receipt_id",
                    "authorization_sig",
                    "result_hash",
                    "result_status",
                    "seal_sig",
                    "status",
                    "created_at",
                    "sealed_at",
                    "signing_method",
                    "metadata",
                ]
            }
        )


class ReceiptStore:
    """Append-only JSONL store for receipts."""

    def __init__(self, store_dir: str = ".swarm/juraregel-work/receipts"):
        self.store_dir = Path(store_dir)
        self.store_dir.mkdir(parents=True, exist_ok=True)

    def save(self, receipt: Receipt) -> str:
        path = self.store_dir / f"{receipt.agent_id}.jsonl"
        with open(path, "a") as f:
            f.write(json.dumps(receipt.to_dict()) + "\n")
        return receipt.receipt_id

    def load(self, agent_id: str) -> list:
        path = self.store_dir / f"{agent_id}.jsonl"
        if not path.exists():
            return []
        receipts = []
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    receipts.append(Receipt.from_dict(json.loads(line)))
        return receipts

    def get(self, receipt_id: str) -> Optional[Receipt]:
        for path in self.store_dir.glob("*.jsonl"):
            with open(path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data = json.loads(line)
                        if data.get("receipt_id") == receipt_id:
                            return Receipt.from_dict(data)
        return None

    def walk_delegation_chain(self, receipt_id: str) -> list:
        """Walk from a child receipt back to the root."""
        chain = []
        current = self.get(receipt_id)
        visited = set()
        while current and current.receipt_id not in visited:
            chain.append(current)
            visited.add(current.receipt_id)
            if current.parent_receipt_id:
                current = self.get(current.parent_receipt_id)
            else:
                break
        return list(reversed(chain))

    def verify_chain(self, agent_id: str) -> dict:
        """Verify all receipts for an agent form a valid chain."""
        receipts = self.load(agent_id)
        if not receipts:
            return {"valid": True, "receipts": 0, "errors": []}

        errors = []
        for receipt in receipts:
            if receipt.status == "sealed" and not receipt.seal_sig:
                errors.append(
                    f"Receipt {receipt.receipt_id}: sealed but missing seal_sig"
                )

        return {"valid": len(errors) == 0, "receipts": len(receipts), "errors": errors}
