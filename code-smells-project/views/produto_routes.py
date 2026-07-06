from flask import Blueprint, request, jsonify
from controllers import produto_controller

produto_bp = Blueprint("produtos", __name__)


@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    result = produto_controller.listar_produtos()
    return jsonify(result), 200


@produto_bp.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None, type=float)
    preco_max = request.args.get("preco_max", None, type=float)

    result = produto_controller.buscar_produtos(termo, categoria, preco_min, preco_max)
    return jsonify(result), 200


@produto_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    result = produto_controller.buscar_produto(produto_id)
    return jsonify(result), 200


@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
    data = request.get_json()
    result = produto_controller.criar_produto(data)
    return jsonify(result), 201


@produto_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    data = request.get_json()
    result = produto_controller.atualizar_produto(produto_id, data)
    return jsonify(result), 200


@produto_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    result = produto_controller.deletar_produto(produto_id)
    return jsonify(result), 200
