from app.models import Customer, Order, OrderDetail, Product
from app.extensions import db, commit_or_rollback

def get_all_customers():
    customers = Customer.query.all()
    return customers


def get_customer_by_id(customer_id):
    customer = db.session.get(Customer, customer_id)
    return customer

def create_customer(data):
    customer = Customer(**data)

    db.session.add(customer)
    commit_or_rollback()

    return customer


def update_customer(customer_id, data):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return None

    for key, value in data.items():
        setattr(customer, key, value)

    commit_or_rollback()

    return customer


def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return False

    db.session.delete(customer)
    commit_or_rollback()

    return True
def get_customer_order_history(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return None

    orders = Order.query.filter_by(
        customer_id=customer_id
    ).all()

    result = []

    for order in orders:
        details = OrderDetail.query.filter_by(
            order_id=order.id
        ).all()

        products = []

        for detail in details:
            product = db.session.get(Product, detail.product_id)

            if product:
                products.append({
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "quantity": float(detail.quantity),
                    "unit_price": float(detail.unit_price),
                    "discount": detail.discount
                })

        result.append({
            "order_id": order.id,
            "order_date": (
                order.order_date.isoformat()
                if order.order_date else None
            ),
            "payment_type": order.payment_type,
            "products": products
        })

    return {
        "customer_id": customer.id,
        "customer_name": (
            f"{customer.first_name or ''} "
            f"{customer.last_name or ''}"
        ).strip(),
        "orders": result
    }