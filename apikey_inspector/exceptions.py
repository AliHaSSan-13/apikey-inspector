class ApiKeyInspectorError(Exception):
    """Base exception for all apikey-inspector errors."""
    pass

class KeyFormatError(ApiKeyInspectorError):
    """Raised when the key fails early regex/format validation."""
    def __init__(self, message: str, detected_pattern: str = ""):
        super().__init__(message)
        self.detected_pattern = detected_pattern

class ProviderNotSupportedError(ApiKeyInspectorError):
    """Raised when a valid-looking key doesn't map to a supported provider."""
    pass

class NetworkError(ApiKeyInspectorError):
    """Raised when an API call times out or fails at the network level."""
    pass
