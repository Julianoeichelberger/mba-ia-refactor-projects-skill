from flask import Blueprint, request, jsonify
from controllers.user_controller import UserController

user_bp = Blueprint('users', __name__)
controller = UserController()


@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify(controller.get_all()), 200


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(controller.get_by_id(user_id)), 200


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    result = controller.create(data)
    return jsonify(result), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    result = controller.update(user_id, data)
    return jsonify(result), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = controller.delete(user_id)
    return jsonify(result), 200


@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
def get_user_tasks(user_id):
    return jsonify(controller.get_user_tasks(user_id)), 200


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result = controller.login(data)
    return jsonify(result), 200
