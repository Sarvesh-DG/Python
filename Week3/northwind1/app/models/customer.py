from app.extensions import db
from sqlalchemy.dialects.mysql import LONGTEXT


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    company = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    email_address = db.Column(db.String(50))
    job_title = db.Column(db.String(50))

    business_phone = db.Column(db.String(25))
    home_phone = db.Column(db.String(25))
    mobile_phone = db.Column(db.String(25))
    fax_number = db.Column(db.String(25))

    address = db.Column(LONGTEXT)
    city = db.Column(db.String(50))
    state_province = db.Column(db.String(50))
    zip_postal_code = db.Column(db.String(15))
    country_region = db.Column(db.String(50))

    web_page = db.Column(LONGTEXT)
    notes = db.Column(LONGTEXT)
    attachments = db.Column(db.LargeBinary)