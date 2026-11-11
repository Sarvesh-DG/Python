import pytest

from app.models import Customer, Order, Product
from app.validators.payload import ValidationError, validate_payload


def test_rejects_unknown_fields():
    with pytest.raises(ValidationError, match="Unknown field"):
        validate_payload(Customer, {"unexpected": "value"})


def test_rejects_wrong_string_type():
    with pytest.raises(ValidationError, match="must be a string"):
        validate_payload(Customer, {"first_name": 123})


def test_rejects_string_over_column_limit():
    with pytest.raises(ValidationError, match="at most 50 characters"):
        validate_payload(Product, {"product_name": "X" * 51})


def test_converts_iso_datetime():
    result = validate_payload(Order, {"order_date": "2026-11-11T10:30:00"})
    assert result["order_date"].isoformat() == "2026-11-11T10:30:00"


def test_rejects_invalid_datetime():
    with pytest.raises(ValidationError, match="ISO 8601"):
        validate_payload(Order, {"order_date": "tomorrow"})


def test_put_replacement_resets_missing_nullable_fields():
    result = validate_payload(Customer, {"first_name": "Grace"}, mode="replace")
    assert result["first_name"] == "Grace"
    assert result["last_name"] is None
    assert "city" in result


def test_rejects_null_for_non_nullable_product_price():
    with pytest.raises(ValidationError, match="cannot be null"):
        validate_payload(Product, {"list_price": None})


def test_rejects_non_boolean_discontinued_flag():
    with pytest.raises(ValidationError, match="must be a boolean"):
        validate_payload(Product, {"discontinued": "false"})
