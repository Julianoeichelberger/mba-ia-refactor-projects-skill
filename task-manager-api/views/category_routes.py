from flask import Blueprint, request, jsonify
from controllers.category_controller import CategoryController

category_bp = Blueprint('categories', __name__)
controller = CategoryController()


@category_bp.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(controller.get_all()), 200


@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    result = controller.create(data)
    return jsonify(result), 201


@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    data = request.get_json()
    result = controller.update(cat_id, data)
    return jsonify(result), 200


@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    result = controller.delete(cat_id)
    return jsonify(result), 200
