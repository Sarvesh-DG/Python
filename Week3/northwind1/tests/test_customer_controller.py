from app.controllers import customer_controller
from app.models import Customer


def test_customer_crud(app):
    with app.app_context():
        customer = customer_controller.create_customer({
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email_address": "ada@example.com",
        })

        assert customer.id is not None
        assert customer_controller.get_customer_by_id(customer.id).first_name == "Ada"
        assert len(customer_controller.get_all_customers()) == 1

        updated = customer_controller.update_customer(
            customer.id, {"city": "London"}
        )
        assert updated.city == "London"

        assert customer_controller.delete_customer(customer.id) is True
        assert customer_controller.get_customer_by_id(customer.id) is None


def test_update_missing_customer_returns_none(app):
    with app.app_context():
        assert customer_controller.update_customer(999, {"city": "Nowhere"}) is None


def test_delete_missing_customer_returns_false(app):
    with app.app_context():
        assert customer_controller.delete_customer(999) is False
