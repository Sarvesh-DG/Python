from app.models import Product
from app.extensions import db, commit_or_rollback


def get_all_products():
    return Product.query.all()


def get_product_by_id(product_id):
    return db.session.get(Product, product_id)


def create_product(data):
    product = Product(**data)

    db.session.add(product)
    commit_or_rollback()

    return product


def update_product(product_id, data):
    product = db.session.get(Product, product_id)

    if not product:
        return None

    for key, value in data.items():
        setattr(product, key, value)

    commit_or_rollback()

    return product


def delete_product(product_id):
    product = db.session.get(Product, product_id)

    if not product:
        return False

    db.session.delete(product)
    commit_or_rollback()

    return True