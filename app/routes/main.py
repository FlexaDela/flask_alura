from flask import Blueprint, jsonify, request
from app.models.user import LoginPayLoad
from pydantic import ValidationError

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/login/', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayLoad(**raw_data)
    except ValidationError as e:
        return jsonify({"error":e.json()}), 400
    except Exception as e:
        return jsonify({"error":"erro durando a requisição"}), 500

    if user_data.username == 'admin' and user_data.password == '123':
        return jsonify({"message":f"Login realizado pelo {user_data.model_dump()}'"}), 200
    else:
        return jsonify({"message":f"Erro nas credenciais"}), 401

@main_bp.route("/product/", methods=['GET'])
def get_products():
    return jsonify({"message":"Listagem de produtos"})


@main_bp.route("/product/<int:id>", methods=['GET'])
def get_product_id(id):
    return jsonify({"message":"Um unico produto"})

@main_bp.route("/product/", methods=['POST'])
def create_product():
    return jsonify({"message":"Criando produto"})

@main_bp.route("/product/<int:id>", methods=['PUT'])
def update_product(id):
    return jsonify({"message":"Atualizando produto"})

@main_bp.route("/product/<int:id>", methods=['PATCH'])
def update_product_partial(id):
    return jsonify({"message":"Atualizando produto"})

@main_bp.route("/product/<int:id>", methods=['DELETE'])
def delete_product(id):
    return jsonify({"message":"Deletando produto"})

@main_bp.route("/")
def index():
    return jsonify({"message":"Bem vindo"})

