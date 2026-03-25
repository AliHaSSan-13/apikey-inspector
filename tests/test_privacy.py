from apikey_inspector.privacy import mask_key, redact_sensitive_data

def test_mask_key_openai():
    assert mask_key("sk-proj-1234567890abcdef") == "sk-proj-1234****cdef"
    assert mask_key("sk-1234567890abcdef") == "sk-1234****cdef"

def test_mask_key_anthropic():
    assert mask_key("sk-ant-api03-1234567890abcdef") == "sk-ant-api03-****cdef"

def test_mask_key_google():
    assert mask_key("AIzaSyAXXXXYYYYZZZZWWWW") == "AIza****WWWW"

def test_mask_key_short():
    assert mask_key("12345") == "****"

def test_redact_sensitive_data():
    data = {
        "status": "active",
        "secret_token": "sk-1234567890abcdef",
        "nested": {
            "password": "my_password",
            "public_id": "123"
        }
    }
    redacted = redact_sensitive_data(data)
    assert redacted["status"] == "active"
    assert redacted["secret_token"] == "sk-1234****cdef"
    assert redacted["nested"]["password"] == "***"
    assert redacted["nested"]["public_id"] == "123"
