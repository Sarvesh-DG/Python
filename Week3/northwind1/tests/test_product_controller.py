from app.controllers import product_controller


def test_product_crud(app):
    with app.app_context():
        product = product_controller.create_product({
            "product_name": "Test tea",
            "product_code": "T-001",
            "list_price": 12.50,
        })

        assert product.id is not None
        assert product_controller.get_product_by_id(product.id).product_name == "Test tea"
        assert len(product_controller.get_all_products()) == 1

        updated = product_controller.update_product(
            product.id, {"category": "Beverages"}
        )
        assert updated.category == "Beverages"

        assert product_controller.delete_product(product.id) is True
        assert product_controller.get_product_by_id(product.id) is None


def test_update_missing_product_returns_none(app):
    with app.app_context():
        assert product_controller.update_product(999, {"category": "Other"}) is None


def test_delete_missing_product_returns_false(app):
    with app.app_context():
        assert product_controller.delete_product(999) is False
