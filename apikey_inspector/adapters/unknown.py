import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyStatus

class UnknownAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.UNKNOWN

    async def inspect(self) -> InspectionResult:
        """Unknown keys just return valid=False."""
        self.result.status = KeyStatus.UNKNOWN
        self.result.errors.append("Unrecognized key prefix.")
        return self.result
