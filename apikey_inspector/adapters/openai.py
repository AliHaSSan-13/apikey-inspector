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
            # 1. Check validity and get models
            models_resp = await self.client.get("https://api.openai.com/v1/models", headers=headers)
            
            if models_resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = models_resp.json()
                self.result.models = [m["id"] for m in data.get("data", [])]
            elif models_resp.status_code == 401:
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("Key is invalid or expired.")
                return self.result
            elif models_resp.status_code == 429:
                self.result.valid = True
                self.result.status = KeyStatus.RATE_LIMITED
                self.result.errors.append("Rate limited while checking models.")

            # 2. Extract rate limits from headers (if any)
            rl_limit = models_resp.headers.get("x-ratelimit-limit-requests")
            rl_remain = models_resp.headers.get("x-ratelimit-remaining-requests")
            if rl_limit:
                self.result.rate_limits = {"limit_requests": rl_limit, "remaining": rl_remain}

            # 3. Check usage / permissions (using standard models check for now)
            # Fetching true usage often requires dashboard APIs which are undocumented, but we do our best.

        except httpx.TimeoutException:
            self.result.errors.append("Connection timed out.")
        except httpx.RequestError as e:
            self.result.errors.append(f"Network error: {str(e)}")

        return self.result
