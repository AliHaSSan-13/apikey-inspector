import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult, UsageInfo
from apikey_inspector.models.provider import Provider, KeyStatus

class OpenAIAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.OPENAI

    async def inspect(self) -> InspectionResult:
        self.result.usage_available = True
        headers = {"Authorization": f"Bearer {self.key}"}

        try:
            resp = await self.client.get("https://api.openai.com/v1/models", headers=headers)
            
            # Extract rate limits regardless of status code
            rl_limit = resp.headers.get("x-ratelimit-limit-requests")
            rl_remain = resp.headers.get("x-ratelimit-remaining-requests")
            if rl_limit:
                self.result.rate_limits = {"limit_requests": rl_limit, "remaining": rl_remain}

            if resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = resp.json()
                self.result.models = [m["id"] for m in data.get("data", [])]
            elif resp.status_code == 401:
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("Key is invalid or expired.")
            elif resp.status_code == 429:
                self.result.valid = True
                self.result.status = KeyStatus.RATE_LIMITED
                self.result.errors.append("Rate limited while checking models.")
                
        except Exception as e:
            self.handle_network_error(e)

        return self.result
