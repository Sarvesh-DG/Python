from app.extensions import db
from sqlalchemy.dialects.mysql import LONGTEXT


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    employee_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)

    order_date = db.Column(db.DateTime)
    shipped_date = db.Column(db.DateTime)

    shipper_id = db.Column(db.Integer)
    ship_name = db.Column(db.String(50))
    ship_address = db.Column(LONGTEXT)
    ship_city = db.Column(db.String(50))
    ship_state_province = db.Column(db.String(50))
    ship_zip_postal_code = db.Column(db.String(50))
    ship_country_region = db.Column(db.String(50))

    shipping_fee = db.Column(db.Numeric(19, 4))
    taxes = db.Column(db.Numeric(19, 4))
    payment_type = db.Column(db.String(50))
    paid_date = db.Column(db.DateTime)

    notes = db.Column(LONGTEXT)
    tax_rate = db.Column(db.Float)