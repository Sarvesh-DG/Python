from unittest.mock import patch, Mock


def test_customer_list_route_uses_controller(client):
    with patch("app.routes.customer_routes.customer_controller.get_all_customers") as mocked:
        mocked.return_value = [
            Mock(id=1, first_name="Ada", last_name="Lovelace",
                 company="Analytical Engines", email_address="ada@example.com")
        ]

        response = client.get("/api/customers/")

    assert response.status_code == 200
    assert response.get_json()[0]["first_name"] == "Ada"
    mocked.assert_called_once_with()


def test_customer_not_found_route(client):
    with patch("app.routes.customer_routes.customer_controller.get_customer_by_id",
               return_value=None):
        response = client.get("/api/customers/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Customer not found"


def test_product_list_route_uses_controller(client):
    with patch("app.routes.product_routes.product_controller.get_all_products") as mocked:
        mocked.return_value = [
            Mock(id=1, product_name="Tea", product_code="T1",
                 list_price=12.5, category="Beverages")
        ]

        response = client.get("/api/products/")

    assert response.status_code == 200
    assert response.get_json()[0]["product_name"] == "Tea"
    mocked.assert_called_once_with()


def test_order_list_route_uses_controller(client):
    with patch("app.routes.order_routes.order_controller.get_all_orders") as mocked:
        mocked.return_value = [
            Mock(id=1, customer_id=7, order_date=None, shipped_date=None,
                 payment_type="Cash", shipping_fee=0)
        ]

        response = client.get("/api/orders/")

    assert response.status_code == 200
    assert response.get_json()[0]["customer_id"] == 7
    mocked.assert_called_once_with()


def test_customer_order_history_route_uses_controller(client):
    expected = {"customer_id": 3, "customer_name": "Test User", "orders": []}
    with patch(
        "app.routes.customer_routes.customer_controller.get_customer_order_history",
        return_value=expected,
    ) as mocked:
        response = client.get("/api/customers/3/order-history")

    assert response.status_code == 200
    assert response.get_json() == expected
    mocked.assert_called_once_with(3)

def test_customer_create_route(client):
    with patch("app.routes.customer_routes.customer_controller.create_customer") as mocked:
        mocked.return_value = Mock(id=42)
        response = client.post("/api/customers/", json={"first_name": "Ada"})
    assert response.status_code == 201
    assert response.get_json()["id"] == 42
    mocked.assert_called_once_with({"first_name": "Ada"})


def test_customer_update_and_delete_routes(client):
    with patch("app.routes.customer_routes.customer_controller.update_customer",
               return_value=Mock()) as update_mock:
        response = client.patch("/api/customers/4", json={"city": "London"})
    assert response.status_code == 200
    update_mock.assert_called_once_with(4, {"city": "London"})

    with patch("app.routes.customer_routes.customer_controller.delete_customer",
               return_value=True) as delete_mock:
        response = client.delete("/api/customers/4")
    assert response.status_code == 200
    delete_mock.assert_called_once_with(4)


def test_product_create_route(client):
    with patch("app.routes.product_routes.product_controller.create_product") as mocked:
        mocked.return_value = Mock(id=21)
        response = client.post("/api/products/", json={"product_name": "Tea"})
    assert response.status_code == 201
    assert response.get_json()["id"] == 21
    mocked.assert_called_once_with({"product_name": "Tea"})


def test_product_update_and_delete_routes(client):
    with patch("app.routes.product_routes.product_controller.update_product",
               return_value=Mock()) as update_mock:
        response = client.patch("/api/products/2", json={"category": "Drinks"})
    assert response.status_code == 200
    update_mock.assert_called_once_with(2, {"category": "Drinks"})

    with patch("app.routes.product_routes.product_controller.delete_product",
               return_value=True) as delete_mock:
        response = client.delete("/api/products/2")
    assert response.status_code == 200
    delete_mock.assert_called_once_with(2)


def test_order_create_route_converts_iso_dates(client):
    from datetime import datetime

    with patch("app.routes.order_routes.order_controller.create_order") as mocked:
        mocked.return_value = Mock(id=31)
        response = client.post(
            "/api/orders/",
            json={"order_date": "2026-11-11T10:30:00", "payment_type": "Cash"},
        )
    assert response.status_code == 201
    passed_data = mocked.call_args.args[0]
    assert passed_data["order_date"] == datetime(2026, 11, 11, 10, 30)


def test_order_update_and_delete_routes(client):
    with patch("app.routes.order_routes.order_controller.update_order",
               return_value=Mock()) as update_mock:
        response = client.patch("/api/orders/8", json={"payment_type": "Card"})
    assert response.status_code == 200
    update_mock.assert_called_once_with(8, {"payment_type": "Card"})

    with patch("app.routes.order_routes.order_controller.delete_order",
               return_value=True) as delete_mock:
        response = client.delete("/api/orders/8")
    assert response.status_code == 200
    delete_mock.assert_called_once_with(8)


def test_unknown_customer_field_is_rejected(client):
    response = client.post(
        "/api/customers/",
        json={"first_name": "Ada", "not_a_column": "unexpected"},
    )
    assert response.status_code == 400
    assert "Unknown field" in response.get_json()["error"]


def test_customer_string_field_type_is_validated(client):
    response = client.post("/api/customers/", json={"first_name": 123})
    assert response.status_code == 400
    assert "must be a string" in response.get_json()["error"]


def test_product_string_length_is_validated(client):
    response = client.post(
        "/api/products/",
        json={"product_name": "P" * 51},
    )
    assert response.status_code == 400
    assert "at most 50 characters" in response.get_json()["error"]


def test_order_date_format_is_validated(client):
    response = client.post(
        "/api/orders/",
        json={"order_date": "not-a-date"},
    )
    assert response.status_code == 400
    assert "ISO 8601" in response.get_json()["error"]


def test_order_numeric_field_is_validated(client):
    response = client.post(
        "/api/orders/",
        json={"shipping_fee": "not-a-number"},
    )
    assert response.status_code == 400
    assert "must be numeric" in response.get_json()["error"]


def test_put_replaces_omitted_customer_fields(client):
    with patch("app.routes.customer_routes.customer_controller.update_customer") as mocked:
        mocked.return_value = Mock()
        response = client.put("/api/customers/9", json={"first_name": "Grace"})

    assert response.status_code == 200
    passed = mocked.call_args.args[1]
    assert passed["first_name"] == "Grace"
    assert passed["last_name"] is None
    assert "city" in passed


def test_patch_only_passes_supplied_customer_fields(client):
    with patch("app.routes.customer_routes.customer_controller.update_customer") as mocked:
        mocked.return_value = Mock()
        response = client.patch("/api/customers/9", json={"city": "London"})

    assert response.status_code == 200
    assert mocked.call_args.args[1] == {"city": "London"}


def test_database_error_returns_safe_conflict_response(client):
    from sqlalchemy.exc import IntegrityError

    with patch(
        "app.routes.customer_routes.customer_controller.create_customer",
        side_effect=IntegrityError("insert", {}, Exception("duplicate")),
    ):
        response = client.post("/api/customers/", json={"first_name": "Ada"})

    assert response.status_code == 409
    assert response.get_json() == {"error": "Database operation failed."}
