import asyncio
import httpx
from typing import List

from apikey_inspector.detector import detect_provider
from apikey_inspector.models.provider import Provider
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.adapters.base import BaseAdapter
from apikey_inspector.adapters.unknown import UnknownAdapter
from apikey_inspector.adapters.openai import OpenAIAdapter
from apikey_inspector.adapters.anthropic import AnthropicAdapter
from apikey_inspector.adapters.google import GoogleAdapter
from apikey_inspector.adapters.huggingface import HuggingFaceAdapter
from apikey_inspector.adapters.cohere import CohereAdapter

ADAPTERS = {
    Provider.OPENAI: OpenAIAdapter,
    Provider.ANTHROPIC: AnthropicAdapter,
    Provider.GOOGLE: GoogleAdapter,
    Provider.HUGGINGFACE: HuggingFaceAdapter,
    Provider.COHERE: CohereAdapter,
}

async def inspect(key: str, client: httpx.AsyncClient, offline: bool = False) -> InspectionResult:
    """Inspects a single API key."""
    provider, key_type = detect_provider(key)
    
    AdapterClass = ADAPTERS.get(provider, UnknownAdapter)
    adapter = AdapterClass(key=key, key_type=key_type, client=client)
    
    if offline:
        # Just return detection in offline mode
        adapter.result.errors.append("Offline mode enabled. Skipped network check.")
        return adapter.result
        
    return await adapter.inspect()

async def inspect_batch(keys: List[str], offline: bool = False) -> List[InspectionResult]:
    """Inspects multiple keys concurrently with per-provider rate limits."""
    # Shared client for efficiency across batch
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Per-provider concurrency limit (e.g., 5 concurrent requests)
        semaphores = {p: asyncio.Semaphore(5) for p in Provider}
        
        async def bounded_inspect(key: str) -> InspectionResult:
            provider, _ = detect_provider(key)
            sem = semaphores.get(provider, semaphores[Provider.UNKNOWN])
            async with sem:
                return await inspect(key, client, offline=offline)
                
        return await asyncio.gather(*(bounded_inspect(k) for k in keys))

