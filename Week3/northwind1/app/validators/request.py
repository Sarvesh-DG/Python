from flask import jsonify, request

from app.validators.payload import ValidationError, validate_payload


def get_validated_json(model, mode="create"):
    """Return (validated_payload, error_response)."""
    payload = request.get_json(silent=True)
    try:
        return validate_payload(model, payload, mode=mode), None
    except ValidationError as exc:
        return None, (jsonify({"error": str(exc)}), 400)
