from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict, Field

from apikey_inspector.models.provider import Provider, KeyType, KeyStatus

class UsageInfo(BaseModel):
    tokens_used_this_month: Optional[int] = None
    cost_this_month: Optional[float] = None
    cost_limit: Optional[float] = None

class InspectionResult(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    provider: Provider
    key_type: KeyType
    key_masked: str
    valid: bool
    status: KeyStatus
    models: List[str] = Field(default_factory=list)
    usage: Optional[UsageInfo] = None
    rate_limits: Optional[Dict[str, Any]] = None
    org_info: Optional[Dict[str, Any]] = None
    permissions: List[str] = Field(default_factory=list)
    usage_available: bool = True
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    errors: List[str] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict without exposing sensitive keys."""
        return self.model_dump()
