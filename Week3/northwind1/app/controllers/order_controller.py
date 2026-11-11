from app.models import Order
from app.extensions import db, commit_or_rollback


def get_all_orders():
    return Order.query.all()


def get_order_by_id(order_id):
    return db.session.get(Order, order_id)


def create_order(data):
    order = Order(**data)

    db.session.add(order)
    commit_or_rollback()

    return order


def update_order(order_id, data):
    order = db.session.get(Order, order_id)

    if not order:
        return None

    for key, value in data.items():
        setattr(order, key, value)

    commit_or_rollback()

    return order


def delete_order(order_id):
    order = db.session.get(Order, order_id)

    if not order:
        return False

    db.session.delete(order)
    commit_or_rollback()

    return True