import httpx

from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.models.provider import Provider, KeyStatus

class HuggingFaceAdapter(BaseAdapter):
    def provider_id(self) -> Provider:
        return Provider.HUGGINGFACE

    async def inspect(self) -> InspectionResult:
        self.result.usage_available = False
        headers = {"Authorization": f"Bearer {self.key}"}

        try:
            # HuggingFace whoami endpoint
            url = "https://huggingface.co/api/whoami-v2"
            resp = await self.client.get(url, headers=headers)
            
            if resp.status_code == 200:
                self.result.valid = True
                self.result.status = KeyStatus.VALID
                data = resp.json()
                
                self.result.org_info = {
                    "username": data.get("name"),
                    "email": data.get("email"),
                    "type": data.get("type")
                }
                
                # Try to map auth permissions
                auth_obj = data.get("auth", {})
                if "accessToken" in auth_obj:
                    self.result.permissions = auth_obj.get("accessToken", {}).get("role", [])
                
                self.result.models = ["<HF Inference Endpoints>"]
                
            elif resp.status_code == 401:
                self.result.valid = False
                self.result.status = KeyStatus.EXPIRED
                self.result.errors.append("HuggingFace token is invalid or expired.")
            else:
                self.result.errors.append(f"Unexpected status code: {resp.status_code}")
                
        except httpx.TimeoutException:
            self.result.errors.append("Connection timed out.")
        except httpx.RequestError as e:
            self.result.errors.append(f"Network error: {str(e)}")

        return self.result
