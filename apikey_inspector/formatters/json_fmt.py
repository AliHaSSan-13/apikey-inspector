import json
from apikey_inspector.models.result import InspectionResult
from apikey_inspector.privacy import redact_sensitive_data

def format_json(result: InspectionResult, redact: bool = True) -> str:
    """Format result as JSON, with optional redaction for embedded secrets."""
    data = result.to_dict()
    if redact:
        data = redact_sensitive_data(data)
    
    # Convert enums/datetimes inside the output to strings if they aren't serialized
    return json.dumps(data, indent=2, default=str)

def format_batch_json(results: list[InspectionResult], redact: bool = True) -> str:
    data = [r.to_dict() for r in results]
    if redact:
        data = [redact_sensitive_data(d) for d in data]
    return json.dumps(data, indent=2, default=str)
