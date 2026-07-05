"""
Government Source Connectors — Base interface.

ponytail: urllib.request ipv requests — stdlib heeft alles wat we nodig hebben
Upgrade pad: rate limiting, retries, caching → httpx/aiohttp
"""
from abc import ABC, abstractmethod
from typing import Optional

class BaseConnector(ABC):
    """Base interface for all government source connectors."""

    @abstractmethod
    def list_sources(self) -> list[dict]:
        """List available sources/documents."""
        pass

    @abstractmethod
    def get_document(self, doc_id: str) -> dict:
        """Get a specific document by ID."""
        pass

    @abstractmethod
    def check_for_updates(self, last_check: str = None) -> list[dict]:
        """Check for new/updated documents since last_check (ISO date)."""
        pass

    @abstractmethod
    def normalize(self, raw_data: str) -> dict:
        """Normalize raw data to structured JSON."""
        pass

    def health_check(self) -> dict:
        """Check if the source endpoint is reachable."""
        return {"source": self.__class__.__name__, "status": "not_implemented"}
