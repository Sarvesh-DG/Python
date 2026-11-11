from flask import Blueprint, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app.controllers import product_controller
from app.models import Product
from app.validators.request import get_validated_json

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["GET"])
def get_products():
    products = product_controller.get_all_products()
    return jsonify([
        {
            "id": p.id,
            "product_name": p.product_name,
            "product_code": p.product_code,
            "list_price": float(p.list_price or 0),
            "category": p.category,
        }
        for p in products
    ]), 200


@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = product_controller.get_product_by_id(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product.id,
        "product_name": product.product_name,
        "product_code": product.product_code,
        "list_price": float(product.list_price or 0),
        "category": product.category,
    }), 200


@product_bp.route("/", methods=["POST"])
def create_product():
    data, error = get_validated_json(Product, "create")
    if error:
        return error
    try:
        product = product_controller.create_product(data)
        return jsonify({
            "message": "Product created successfully",
            "id": product.id,
        }), 201
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@product_bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data, error = get_validated_json(Product, "replace")
    if error:
        return error
    try:
        product = product_controller.update_product(product_id, data)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product replaced successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@product_bp.route("/<int:product_id>", methods=["PATCH"])
def patch_product(product_id):
    data, error = get_validated_json(Product, "patch")
    if error:
        return error
    try:
        product = product_controller.update_product(product_id, data)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product partially updated"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409


@product_bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    try:
        deleted = product_controller.delete_product(product_id)
        if not deleted:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"message": "Product deleted successfully"}), 200
    except SQLAlchemyError:
        return jsonify({"error": "Database operation failed."}), 409
