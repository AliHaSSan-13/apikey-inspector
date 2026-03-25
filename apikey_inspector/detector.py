import re
from typing import Tuple

from apikey_inspector.models.provider import Provider, KeyType
from apikey_inspector.exceptions import KeyFormatError

def detect_provider(key: str) -> Tuple[Provider, KeyType]:
    """Detects provider and key type without making network requests."""
    
    if not key or not isinstance(key, str):
        raise KeyFormatError("Key must be a non-empty string.")

    # OpenAI
    if key.startswith("sk-proj-"):
        return Provider.OPENAI, KeyType.PROJECT_KEY
    if key.startswith("sk-") and len(key) == 51:
        return Provider.OPENAI, KeyType.USER_KEY

    # Anthropic
    if key.startswith("sk-ant-api03-"):
        return Provider.ANTHROPIC, KeyType.API_KEY

    # Google Gemini
    if key.startswith("AIza") and len(key) == 39:
        return Provider.GOOGLE, KeyType.API_KEY

    # HuggingFace
    if key.startswith("hf_"):
        return Provider.HUGGINGFACE, KeyType.USER_KEY

    # Cohere
    # Cohere keys are typically 40 characters of random alphanumerics
    if re.match(r"^[a-zA-Z0-9]{40}$", key):
        return Provider.COHERE, KeyType.API_KEY
    
    # Together AI
    # Typically 64 characters of random hex or alphanumerics
    if re.match(r"^[a-fA-F0-9]{64}$", key):
        return Provider.TOGETHER, KeyType.API_KEY

    return Provider.UNKNOWN, KeyType.UNKNOWN
