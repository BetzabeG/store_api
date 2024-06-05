from flask import Blueprint, request, jsonify
from models.product_model import Product
from views.product_view import render_product_list, render_product_detail
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identify
from functools import wraps

product_bp = Blueprint("product", __name__)
def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    return wrapper

@product_bp.route("/products", methods=["GET"])
@jwt_required
def get_products():
    products = Product.get_all()
    return jsonify(render_product_list(products))

@product_bp.route("/products/<int:id>", methods=["GET"])
@jwt_required
def get_product(id):
    product = Product.get_by_id(id)
    if Product:
        return jsonify(render_product_detail(product))
    return jsonify({"error":"Producto no encontrado"}), 404

@product_bp.route("/products", methods=["POST"])
@jwt_required
def create_product():
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    
    if not name or not description or not price or stock is None:
        return jsonify({"error": "Faltan datos requeridos"}), 400
    product = Product(name=name, description=description, price=price,stock=stock)
    product.save()
    return jsonify(render_product_detail(product)), 201

@product_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required
def update_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    data = request.json
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")
    stock = data.get("stock")
    
    product.update(name=name, description=description, price=price, stock=stock)
    return jsonify(render_product_detail(product))

@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required
def delete_product(id):
    product = Product.get_by_id(id)
    if not product:
        return jsonify({"error": "Producto no encontrado"}),404
    product.delete()
    return "", 204
    