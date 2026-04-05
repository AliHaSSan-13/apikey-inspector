import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyStatus

class GoogleAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.GOOGLE

    async def inspect(self) -> InspectionResult:
        self.result.usage_available = False
        
        try:
            # Use params to keep the key out of the URL string representation
            url = "https://generativelanguage.googleapis.com/v1beta/models"
            resp = await self.client.get(url, params={"key": self.key})
            
            if resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = resp.json()
                self.result.models = [model.get("name").split("/")[-1] for model in data.get("models", [])]
            elif resp.status_code in (400, 403, 401):
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("Google key is invalid or lacks necessary permissions.")
            elif resp.status_code == 429:
                self.result.valid = True
                self.result.status = KeyStatus.RATE_LIMITED
                self.result.errors.append("Rate limited while checking Google models.")
            else:
                self.result.errors.append(f"Unexpected status code: {resp.status_code}")
                
        except Exception as e:
            self.handle_network_error(e)

        return self.result
