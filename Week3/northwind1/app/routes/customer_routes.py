from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.controllers import customer_controller
from app.models import Customer
from app.validators.request import get_validated_json

customer_bp = Blueprint("customers", __name__)


@customer_bp.route("/", methods=["GET"])
def get_customers():
    customers = customer_controller.get_all_customers()
    return jsonify([
        {
            "id": c.id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "company": c.company,
            "email_address": c.email_address,
        }
        for c in customers
    ]), 200


@customer_bp.route("/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = customer_controller.get_customer_by_id(customer_id)
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({
        "id": customer.id,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "company": customer.company,
        "email_address": customer.email_address,
    }), 200


@customer_bp.route("/", methods=["POST"])
def create_customer():
    data, error = get_validated_json(Customer, "create")
    if error:
        return error
    try:
        customer = customer_controller.create_customer(data)
        return jsonify({
            "message": "Customer created successfully",
            "id": customer.id,
        }), 201
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@customer_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    data, error = get_validated_json(Customer, "replace")
    if error:
        return error
    try:
        customer = customer_controller.update_customer(customer_id, data)
        if customer is None:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify({"message": "Customer replaced successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@customer_bp.route("/<int:customer_id>", methods=["PATCH"])
def patch_customer(customer_id):
    data, error = get_validated_json(Customer, "patch")
    if error:
        return error
    try:
        customer = customer_controller.update_customer(customer_id, data)
        if customer is None:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify({"message": "Customer partially updated"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        deleted = customer_controller.delete_customer(customer_id)
        if not deleted:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify({"message": "Customer deleted successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@customer_bp.route("/<int:customer_id>/order-history", methods=["GET"])
def customer_order_history(customer_id):
    history = customer_controller.get_customer_order_history(customer_id)
    if history is None:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(history), 200
