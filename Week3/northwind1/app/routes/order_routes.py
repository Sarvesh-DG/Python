from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.controllers import order_controller
from app.models import Order
from app.validators.request import get_validated_json

order_bp = Blueprint("orders", __name__)


def serialize_order(order):
    return {
        "id": order.id,
        "customer_id": order.customer_id,
        "order_date": order.order_date.isoformat() if order.order_date else None,
        "shipped_date": order.shipped_date.isoformat() if order.shipped_date else None,
        "payment_type": order.payment_type,
        "shipping_fee": float(order.shipping_fee or 0),
    }


@order_bp.route("/", methods=["GET"])
def get_orders():
    orders = order_controller.get_all_orders()
    return jsonify([serialize_order(order) for order in orders]), 200


@order_bp.route("/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = order_controller.get_order_by_id(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(serialize_order(order)), 200


@order_bp.route("/", methods=["POST"])
def create_order():
    data, error = get_validated_json(Order, "create")
    if error:
        return error
    try:
        order = order_controller.create_order(data)
        return jsonify({
            "message": "Order created successfully",
            "id": order.id,
        }), 201
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@order_bp.route("/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data, error = get_validated_json(Order, "replace")
    if error:
        return error
    try:
        order = order_controller.update_order(order_id, data)
        if order is None:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Order replaced successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@order_bp.route("/<int:order_id>", methods=["PATCH"])
def patch_order(order_id):
    data, error = get_validated_json(Order, "patch")
    if error:
        return error
    try:
        order = order_controller.update_order(order_id, data)
        if order is None:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Order partially updated"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@order_bp.route("/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        deleted = order_controller.delete_order(order_id)
        if not deleted:
            return jsonify({"error": "Order not found"}), 404
        return jsonify({"message": "Order deleted successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409
