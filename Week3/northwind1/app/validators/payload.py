from datetime import datetime
from decimal import Decimal, InvalidOperation
from math import isfinite

from sqlalchemy import Boolean, DateTime, Float, Integer, Numeric, String


class ValidationError(ValueError):
    """Raised when an API request payload does not match the model schema."""


EXCLUDED_FIELDS = {"id", "attachments"}


def _convert_value(field, value, column):
    if value is None:
        if not column.nullable:
            raise ValidationError(f"'{field}' cannot be null.")
        return None

    column_type = column.type

    if isinstance(column_type, Boolean):
        if not isinstance(value, bool):
            raise ValidationError(f"'{field}' must be a boolean.")
        return value

    if isinstance(column_type, DateTime):
        if isinstance(value, datetime):
            return value
        if not isinstance(value, str):
            raise ValidationError(f"'{field}' must be an ISO 8601 datetime string.")
        try:
            return datetime.fromisoformat(value)
        except ValueError as exc:
            raise ValidationError(
                f"'{field}' must use a valid ISO 8601 datetime, e.g. 2026-11-11T10:30:00."
            ) from exc

    if isinstance(column_type, Integer):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValidationError(f"'{field}' must be an integer.")
        return value

    if isinstance(column_type, Float):
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValidationError(f"'{field}' must be numeric.")
        try:
            number = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValidationError(f"'{field}' must be numeric.") from exc
        if not number.is_finite():
            raise ValidationError(f"'{field}' must be a finite number.")
        return float(number)

    if isinstance(column_type, Numeric):
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise ValidationError(f"'{field}' must be numeric.")
        try:
            number = Decimal(str(value))
        except InvalidOperation as exc:
            raise ValidationError(f"'{field}' must be numeric.") from exc
        if not number.is_finite():
            raise ValidationError(f"'{field}' must be a finite number.")
        return number

    if isinstance(column_type, String):
        if not isinstance(value, str):
            raise ValidationError(f"'{field}' must be a string.")
        if column_type.length and len(value) > column_type.length:
            raise ValidationError(
                f"'{field}' must be at most {column_type.length} characters."
            )
        return value

    return value


def validate_payload(model, payload, mode="create"):
    """Validate and normalize a JSON object against an ORM model.

    Modes:
      create: validate only supplied fields and let ORM defaults apply.
      patch: validate only supplied fields.
      replace: PUT semantics; omitted writable fields are reset to their
               model default or None.
    """
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")
    if not payload:
        raise ValidationError("Request body is required.")

    columns = {
        column.name: column
        for column in model.__table__.columns
        if column.name not in EXCLUDED_FIELDS and not column.primary_key
    }

    unknown = sorted(set(payload) - set(columns))
    if unknown:
        raise ValidationError(f"Unknown field(s): {', '.join(unknown)}.")

    source = dict(payload)
    if mode == "replace":
        replacement = {}
        for name, column in columns.items():
            if name in source:
                replacement[name] = source[name]
            elif column.default is not None and not callable(column.default.arg):
                replacement[name] = column.default.arg
            else:
                replacement[name] = None
        source = replacement

    validated = {}
    for name, value in source.items():
        validated[name] = _convert_value(name, value, columns[name])

    return validated
