from flask import Blueprint, jsonify

main_bp = Blueprint("main_bp", __name__)

@main_bp.route('/login/', methods=['POST'])
def login():
    return jsonify({"message":"Tela de Login"})

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

