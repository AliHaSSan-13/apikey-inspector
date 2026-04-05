import re

def mask_key(key: str) -> str:
    """Masks an API key to display only the start and end.
    
    Examples:
        sk-1234567890abcdef1234567890abcdef -> sk-1234****cdef
        AIzaSyAXXXXYYYYZZZZWWWW -> AIza****WWWW
    """
    if not key or len(key) < 8:
        return "****"
    
    # Check common prefixes to keep them visible
    if key.startswith("sk-proj-"):
        prefix_len = 12
    elif key.startswith("sk-ant-api"):
        prefix_len = 13
    elif key.startswith("sk-"):
        prefix_len = 7
    elif key.startswith("AIza"):
        prefix_len = 4
    elif key.startswith("hf_"):
        prefix_len = 6
    else:
        prefix_len = max(4, len(key) // 6)
        
    suffix_len = 4
    if len(key) <= prefix_len + suffix_len:
        return f"{key[:prefix_len]}****"
        
    return f"{key[:prefix_len]}****{key[-suffix_len:]}"

def redact_sensitive_data(data: dict) -> dict:
    """Recursively redacts potentially sensitive information from a dictionary."""
    redacted = {}
    for k, v in data.items():
        if isinstance(v, dict):
            redacted[k] = redact_sensitive_data(v)
        elif isinstance(v, (list, tuple, set)):
            # Handle collections
            redacted[k] = [redact_sensitive_data(i) if isinstance(i, dict) else i for i in v]
        elif isinstance(k, str) and any(word in k.lower() for word in ['secret', 'token', 'key', 'password']):
            if "password" in k.lower():
                redacted[k] = "***"
            elif isinstance(v, str):
                redacted[k] = mask_key(v)
            else:
                redacted[k] = "***"

        else:
            redacted[k] = v
    return redacted
