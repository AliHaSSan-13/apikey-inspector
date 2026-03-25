import pytest
from apikey_inspector.detector import detect_provider
from apikey_inspector.models.provider import Provider, KeyType
from apikey_inspector.exceptions import KeyFormatError

def test_detect_openai():
    provider, key_type = detect_provider("sk-proj-1234")
    assert provider == Provider.OPENAI
    assert key_type == KeyType.PROJECT_KEY

    provider, key_type = detect_provider("sk-" + "a" * 48)
    assert provider == Provider.OPENAI
    assert key_type == KeyType.USER_KEY

def test_detect_anthropic():
    provider, key_type = detect_provider("sk-ant-api03-1234")
    assert provider == Provider.ANTHROPIC
    assert key_type == KeyType.API_KEY

def test_detect_google():
    # 39 chars starting with AIza
    key = "AIza" + "a" * 35
    provider, key_type = detect_provider(key)
    assert provider == Provider.GOOGLE
    assert key_type == KeyType.API_KEY

def test_detect_huggingface():
    provider, key_type = detect_provider("hf_1234abcdef")
    assert provider == Provider.HUGGINGFACE
    assert key_type == KeyType.USER_KEY

def test_detect_unknown():
    provider, key_type = detect_provider("randomstring")
    assert provider == Provider.UNKNOWN
    assert key_type == KeyType.UNKNOWN

def test_empty_string():
    with pytest.raises(KeyFormatError):
        detect_provider("")
