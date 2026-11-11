from app.extensions import db


class OrderDetail(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer)

    quantity = db.Column(db.Numeric(18, 4), nullable=False, default=0)
    unit_price = db.Column(db.Numeric(19, 4), default=0)
    discount = db.Column(db.Float, nullable=False, default=0)

    status_id = db.Column(db.Integer)
    date_allocated = db.Column(db.DateTime)

    purchase_order_id = db.Column(db.Integer)
    inventory_id = db.Column(db.Integer)