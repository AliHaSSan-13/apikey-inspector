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
            # Google Gemini models endpoint
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.key}"
            resp = await self.client.get(url)
            
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
                
        except httpx.TimeoutException:
            self.result.errors.append("Connection timed out.")
        except httpx.RequestError as e:
            self.result.errors.append(f"Network error: {str(e)}")

        return self.result
