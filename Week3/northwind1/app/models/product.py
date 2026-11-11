from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    product_code = db.Column(db.String(25))
    product_name = db.Column(db.String(50))
    description = db.Column(db.Text)

    standard_cost = db.Column(db.Numeric(19, 4), default=0)
    list_price = db.Column(db.Numeric(19, 4), nullable=False, default=0)

    reorder_level = db.Column(db.Integer)
    target_level = db.Column(db.Integer)
    quantity_per_unit = db.Column(db.String(50))

    discontinued = db.Column(db.Boolean, nullable=False, default=False)
    minimum_reorder_quantity = db.Column(db.Integer)
    category = db.Column(db.String(50))

    attachments = db.Column(db.LargeBinary)