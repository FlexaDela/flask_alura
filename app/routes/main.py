from flask import Blueprint, jsonify, request
from app.models.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.products import Product, ProdctDBModel

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

@main_bp.route("/products/", methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProdctDBModel(**product).model_dump(by_alias=True) for product in products_cursor]
    return jsonify(products_list)


@main_bp.route("/products/<string:id>", methods=['GET'])
def get_product_id(id):
    try:
        oid = ObjectId(id)
    except Exception as e:
        return jsonify({"error":f"Erro ao buscar o produto{id}: {e}"}), 500

    product_cursor = db.products.find_one({'_id': oid})

    if product_cursor:
        product_model = ProdctDBModel(**product_cursor).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_model), 200
    else:
        return jsonify({"error":f"Produto {id} nao encontrado"}), 404

@main_bp.route("/products/", methods=['POST'])
def create_product():
    return jsonify({"message":"Criando produto"})

@main_bp.route("/products/<int:id>", methods=['PUT'])
def update_product(id):
    return jsonify({"message":"Atualizando produto"})

@main_bp.route("/products/<int:id>", methods=['PATCH'])
def update_product_partial(id):
    return jsonify({"message":"Atualizando produto"})

@main_bp.route("/products/<int:id>", methods=['DELETE'])
def delete_product(id):
    return jsonify({"message":"Deletando produto"})

@main_bp.route("/")
def index():
    return jsonify({"message":"Bem vindo"})

