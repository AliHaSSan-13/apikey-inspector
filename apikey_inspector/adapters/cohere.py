import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyStatus

class CohereAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.COHERE

    async def inspect(self) -> InspectionResult:
        self.result.usage_available = False
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Accept": "application/json"
        }

        try:
            # Check models endpoint for validity
            url = "https://api.cohere.com/v1/models"
            resp = await self.client.get(url, headers=headers)
            
            if resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = resp.json()
                self.result.models = [model.get("name") for model in data.get("models", [])]
            elif resp.status_code in (401, 403):
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("Cohere token is invalid or expired.")
            elif resp.status_code == 429:
                self.result.valid = True
                self.result.status = KeyStatus.RATE_LIMITED
                self.result.errors.append("Rate limited while checking Cohere API.")
            else:
                self.result.errors.append(f"Unexpected status code: {resp.status_code} - {resp.text}")
                
        except httpx.TimeoutException:
            self.result.errors.append("Connection timed out.")
        except httpx.RequestError as e:
            self.result.errors.append(f"Network error: {str(e)}")

        return self.result
