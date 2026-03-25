from enum import Enum

class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    TOGETHER = "together"
    UNKNOWN = "unknown"

class KeyType(str, Enum):
    API_KEY = "api_key"
    USER_KEY = "user_key"
    PROJECT_KEY = "project_key"
    UNKNOWN = "unknown"

class KeyStatus(str, Enum):
    VALID = "valid"
    EXPIRED = "expired"
    RATE_LIMITED = "rate_limited"
    UNKNOWN = "unknown"
