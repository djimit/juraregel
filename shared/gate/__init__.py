"""Gate module — bilateral receipt system for AI compliance.

Ported from AIR Blackbox (Apache-2.0). Provides:
- Covenant-based policy enforcement (YAML)
- Ed25519-signed bilateral receipts (authorize + seal)
- Delegation chain verification
"""

from .covenant import Covenant, load_covenant
from .receipt import Receipt, ReceiptStore
from .engine import Gate

__all__ = ["Covenant", "load_covenant", "Receipt", "ReceiptStore", "Gate"]
