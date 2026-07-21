from flask import Blueprint, request, jsonify
from controllers.category_controller import CategoryController
from middlewares.auth import auth_required

category_bp = Blueprint('categories', __name__)
controller = CategoryController()


@category_bp.route('/categories', methods=['GET'])
@auth_required()
def get_categories():
    return jsonify(controller.get_all()), 200


@category_bp.route('/categories', methods=['POST'])
@auth_required()
def create_category():
    data = request.get_json()
    result = controller.create(data)
    return jsonify(result), 201


@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
@auth_required()
def update_category(cat_id):
    data = request.get_json()
    result = controller.update(cat_id, data)
    return jsonify(result), 200


@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
@auth_required(roles=['admin'])
def delete_category(cat_id):
    result = controller.delete(cat_id)
    return jsonify(result), 200
