from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.procuts import Product, ProdctDBModel
from app.decorators import token_required 
from datetime import datetime, timedelta, timezone
import jwt

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
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
            },

            current_app.config['SECRET_KEY'],
            algorithm="HS256"
        )
        return jsonify({"token":token}), 200

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

@main_bp.route("/products", methods=['POST'])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()}), 400

    result = db.product.insert_one(product.model_dump())

    db.products.insert_one(product.model_dump(by_alias=True))
    return jsonify({"message":"Produto criado com sucesso"}), 201

@main_bp.route("/products/<string:id>", methods=['PUT'])
@token_required
def update_product(token, id):
    try:
        oid = ObjectId(id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()}), 400

    update_result = db.products.update_one({'_id': oid}, {'$set': update_data.model_dump(by_alias=True)})

    if update_result.modified_count == 0:
        return jsonify({"error":"Produto nao encontrado"}), 404

    
    updated_product = db.products.find_one({'_id': oid})
    return jsonify(ProdctDBModel(**updated_product).model_dump(by_alias=True, exclude_none=True)), 200

@main_bp.route("/products/<string:id>", methods=['DELETE'])
@token_required
def delete_product(token, id):
    try:
        oid = ObjectId(id)
    except Exception as e:
        return jsonify({"error":f"Erro ao deletar o produto{id}: {e}"}), 500

    delete_result = db.products.delete_one({'_id': oid})

    if delete_result.deleted_count == 0:
        return jsonify({"error":"Produto nao encontrado"}), 404
    return jsonify({"message":"Produto deletado com sucesso"}), 200

@main_bp.route("/")
def index():
    return jsonify({"message":"Bem vindo"})

