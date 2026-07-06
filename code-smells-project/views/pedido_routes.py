from flask import Blueprint, request, jsonify
from controllers import pedido_controller

pedido_bp = Blueprint("pedidos", __name__)


@pedido_bp.route("/pedidos", methods=["POST"])
def criar_pedido():
    data = request.get_json()
    result = pedido_controller.criar_pedido(data)
    return jsonify(result), 201


@pedido_bp.route("/pedidos", methods=["GET"])
def listar_todos_pedidos():
    result = pedido_controller.listar_todos_pedidos()
    return jsonify(result), 200


@pedido_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
def listar_pedidos_usuario(usuario_id):
    result = pedido_controller.listar_pedidos_usuario(usuario_id)
    return jsonify(result), 200


@pedido_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
def atualizar_status_pedido(pedido_id):
    data = request.get_json()
    result = pedido_controller.atualizar_status_pedido(pedido_id, data)
    return jsonify(result), 200


@pedido_bp.route("/relatorios/vendas", methods=["GET"])
def relatorio_vendas():
    result = pedido_controller.relatorio_vendas()
    return jsonify(result), 200
