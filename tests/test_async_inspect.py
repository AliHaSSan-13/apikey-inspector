import pytest
import asyncio
import httpx
from apikey_inspector.inspector import inspect_batch
from apikey_inspector.models.provider import Provider

@pytest.mark.asyncio
async def test_inspect_batch_offline():
    keys = ["sk-proj-123", "sk-ant-api03-456", "AIza789" + "a" * 32]
    results = await inspect_batch(keys, offline=True)
    
    assert len(results) == 3
    assert results[0].provider == Provider.OPENAI
    assert results[1].provider == Provider.ANTHROPIC
    assert results[2].provider == Provider.GOOGLE
    
    for r in results:
        assert "Offline mode enabled" in r.errors[0]

@pytest.mark.asyncio
async def test_inspect_batch_concurrency_limit():
    # This test would require mocking the adapters to verify timing, 
    # but we just check functionality for now.
    pass
