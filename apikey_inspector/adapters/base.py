import abc
import httpx
from datetime import datetime, timezone

from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyType, KeyStatus
from apikey_inspector.privacy import mask_key

class BaseAdapter(abc.ABC):
    def __init__(self, key: str, key_type: KeyType, client: httpx.AsyncClient):
        self.key = key
        self.key_type = key_type
        self.client = client
        self.result = InspectionResult(
            provider=self.provider_id(),
            key_type=key_type,
            key_masked=mask_key(key),
            valid=False,
            status=KeyStatus.UNKNOWN,
            fetched_at=datetime.now(timezone.utc)
        )

    @abc.abstractmethod
    def provider_id(self) -> Provider:
        pass

    @abc.abstractmethod
    async def inspect(self) -> InspectionResult:
        """Perform provider-specific checks and return the populated InspectionResult."""
        pass
