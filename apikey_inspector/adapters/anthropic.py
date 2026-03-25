import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyStatus

class AnthropicAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.ANTHROPIC

    async def inspect(self) -> InspectionResult:
        self.result.usage_available = False # Anthropic doesn't expose usage via API typically
        
        headers = {
            "x-api-key": self.key,
            "anthropic-version": "2023-06-01"
        }

        try:
            # We check the models list to verify validity
            resp = await self.client.get("https://api.anthropic.com/v1/models", headers=headers)
            
            if resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = resp.json()
                self.result.models = [m["id"] for m in data.get("data", [])]
                
                # Extract rate limiting info if present
                rl_limit = resp.headers.get("anthropic-ratelimit-requests-limit")
                rl_remain = resp.headers.get("anthropic-ratelimit-requests-remaining")
                if rl_limit:
                    self.result.rate_limits = {"limit_requests": rl_limit, "remaining": rl_remain}
            
            elif resp.status_code == 401:
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("Anthropic key is invalid or expired.")
            elif resp.status_code == 429:
                self.result.valid = True
                self.result.status = KeyStatus.RATE_LIMITED
                self.result.errors.append("Rate limited while checking Anthropic.")
            else:
                self.result.errors.append(f"Unexpected status code: {resp.status_code}")
                
        except httpx.TimeoutException:
            self.result.errors.append("Connection timed out.")
        except httpx.RequestError as e:
            self.result.errors.append(f"Network error: {str(e)}")

        return self.result
