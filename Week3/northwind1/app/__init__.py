from flask import Flask
from config import Config
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from app import models
    from app.routes.customer_routes import customer_bp
    from app.routes.product_routes import product_bp
    from app.routes.order_routes import order_bp

    app.register_blueprint(customer_bp, url_prefix="/api/customers")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(order_bp, url_prefix="/api/orders")

    return app
