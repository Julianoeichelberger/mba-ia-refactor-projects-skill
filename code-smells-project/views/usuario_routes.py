from flask import Blueprint, request, jsonify
from controllers import usuario_controller

usuario_bp = Blueprint("usuarios", __name__)


@usuario_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    result = usuario_controller.listar_usuarios()
    return jsonify(result), 200


@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
def buscar_usuario(usuario_id):
    result = usuario_controller.buscar_usuario(usuario_id)
    return jsonify(result), 200


@usuario_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    result = usuario_controller.criar_usuario(data)
    return jsonify(result), 201


@usuario_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    result = usuario_controller.login(data)
    return jsonify(result), 200
