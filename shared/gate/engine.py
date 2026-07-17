"""Engine — Gate authorization + sealing with Ed25519 or HMAC-SHA256."""

import hashlib
import hmac
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .covenant import Covenant
from .receipt import Receipt, ReceiptStore

try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False


class Gate:
    """Pre-execution policy enforcement with bilateral receipts."""

    def __init__(
        self,
        covenant: Covenant,
        key_path: Optional[str] = None,
        store_dir: str = ".swarm/juraregel-work/receipts",
    ):
        self.covenant = covenant
        self.store = ReceiptStore(store_dir)
        self.key_path = key_path or os.path.join(store_dir, f"{covenant.agent}.key")
        self._private_key = None
        self._public_key = None
        self._hmac_key = None
        self._load_or_generate_keys()

    def _load_or_generate_keys(self):
        key_file = Path(self.key_path)
        if HAS_CRYPTO:
            if key_file.exists():
                self._private_key = serialization.load_pem_private_key(
                    key_file.read_bytes(), password=None
                )
                self._public_key = self._private_key.public_key()
            else:
                self._private_key = Ed25519PrivateKey.generate()
                self._public_key = self._private_key.public_key()
                key_file.parent.mkdir(parents=True, exist_ok=True)
                key_file.write_bytes(
                    self._private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption(),
                    )
                )
        else:
            if key_file.exists():
                self._hmac_key = key_file.read_bytes()
            else:
                self._hmac_key = os.urandom(32)
                key_file.parent.mkdir(parents=True, exist_ok=True)
                key_file.write_bytes(self._hmac_key)

    def authorize(
        self,
        agent_id: str,
        action_name: str,
        payload: dict,
        context: dict = None,
        parent_receipt_id: str = None,
    ) -> Receipt:
        """Phase 1: Check covenant and sign authorization decision."""
        evaluation = self.covenant.evaluate(action_name, context or {})
        payload_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()[:16]

        authorized = evaluation["decision"] in ("permit", "require_approval")

        receipt = Receipt(
            receipt_id=str(uuid.uuid4()),
            agent_id=agent_id,
            action_name=action_name,
            payload_hash=payload_hash,
            covenant_hash=self.covenant.hash,
            decision=evaluation["decision"],
            authorized=authorized,
            parent_receipt_id=parent_receipt_id,
            status="pending",
            signing_method="ed25519" if HAS_CRYPTO else "hmac-sha256",
            metadata={"rule_matched": evaluation["rule_matched"]},
        )

        # Sign the authorization
        auth_data = f"{receipt.receipt_id}:{receipt.agent_id}:{receipt.action_name}:{receipt.decision}:{receipt.payload_hash}:{receipt.covenant_hash}"
        receipt.authorization_sig = self._sign(auth_data)

        self.store.save(receipt)
        return receipt

    def seal(self, receipt: Receipt, result: dict, status: str = "success") -> Receipt:
        """Phase 2: Bind execution result to authorization."""
        result_hash = hashlib.sha256(
            json.dumps(result, sort_keys=True).encode()
        ).hexdigest()[:16]
        receipt.result_hash = result_hash
        receipt.result_status = status
        receipt.sealed_at = datetime.now(timezone.utc).isoformat()
        receipt.status = "sealed"

        # Sign the seal
        seal_data = (
            f"{receipt.receipt_id}:{receipt.authorization_sig}:{result_hash}:{status}"
        )
        receipt.seal_sig = self._sign(seal_data)

        self.store.save(receipt)
        return receipt

    def verify(self, receipt: Receipt) -> dict:
        """Verify receipt signatures."""
        auth_data = f"{receipt.receipt_id}:{receipt.agent_id}:{receipt.action_name}:{receipt.decision}:{receipt.payload_hash}:{receipt.covenant_hash}"
        auth_valid = self._verify(auth_data, receipt.authorization_sig)

        seal_valid = True
        if receipt.status == "sealed":
            seal_data = f"{receipt.receipt_id}:{receipt.authorization_sig}:{receipt.result_hash}:{receipt.result_status}"
            seal_valid = self._verify(seal_data, receipt.seal_sig)

        return {
            "authorization_valid": auth_valid,
            "seal_valid": seal_valid,
            "overall": auth_valid and seal_valid,
            "signing_method": receipt.signing_method,
        }

    def walk_delegation_chain(self, receipt_id: str) -> list:
        return self.store.walk_delegation_chain(receipt_id)

    def _sign(self, data: str) -> str:
        if HAS_CRYPTO and self._private_key:
            sig = self._private_key.sign(data.encode())
            return sig.hex()[:64]
        else:
            return hmac.new(
                self._hmac_key or b"fallback", data.encode(), hashlib.sha256
            ).hexdigest()[:64]

    def _verify(self, data: str, signature: str) -> bool:
        expected = self._sign(data)
        return hmac.compare_digest(expected, signature)
