from flask import Blueprint, request, jsonify
from models.user_model import User
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

user_bp = Blueprint("user", __name__)
@user_bp.route("/registrer", methods=["POST"])
def registrer():
    data = data.get("username")
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contrasena"}), 400
    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya esta en uso"}), 400
    new_user = User(username, password)
    new_user.save()
    
    return jsonify({"message": "Usuario creado existosamente"}), 201
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    user = User.find_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identify=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales invalidas"}), 401