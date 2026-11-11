from datetime import datetime

from app.controllers import customer_controller, order_controller
from app.extensions import db
from app.models import Customer, Order, OrderDetail, Product


def test_order_crud(app):
    with app.app_context():
        order = order_controller.create_order({
            "customer_id": 1,
            "order_date": datetime(2026, 11, 11, 10, 30),
            "payment_type": "Cash",
        })

        assert order.id is not None
        assert order_controller.get_order_by_id(order.id).payment_type == "Cash"
        assert len(order_controller.get_all_orders()) == 1

        updated = order_controller.update_order(
            order.id, {"payment_type": "Card"}
        )
        assert updated.payment_type == "Card"

        assert order_controller.delete_order(order.id) is True
        assert order_controller.get_order_by_id(order.id) is None


def test_update_missing_order_returns_none(app):
    with app.app_context():
        assert order_controller.update_order(999, {"payment_type": "Card"}) is None


def test_delete_missing_order_returns_false(app):
    with app.app_context():
        assert order_controller.delete_order(999) is False


def test_customer_order_history_includes_products(app):
    with app.app_context():
        customer = Customer(first_name="Grace", last_name="Hopper")
        product = Product(product_name="Compiler book", list_price=25)
        db.session.add_all([customer, product])
        db.session.flush()

        order = Order(customer_id=customer.id, order_date=datetime(2026, 11, 11))
        db.session.add(order)
        db.session.flush()

        detail = OrderDetail(
            order_id=order.id,
            product_id=product.id,
            quantity=2,
            unit_price=25,
            discount=0,
        )
        db.session.add(detail)
        db.session.commit()

        history = customer_controller.get_customer_order_history(customer.id)

        assert history["customer_name"] == "Grace Hopper"
        assert len(history["orders"]) == 1
        assert history["orders"][0]["products"][0]["product_name"] == "Compiler book"
        assert history["orders"][0]["products"][0]["quantity"] == 2.0


def test_order_history_for_missing_customer_returns_none(app):
    with app.app_context():
        assert customer_controller.get_customer_order_history(999) is None
