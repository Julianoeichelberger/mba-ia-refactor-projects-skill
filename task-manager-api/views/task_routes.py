from flask import Blueprint, request, jsonify
from controllers.task_controller import TaskController

task_bp = Blueprint('tasks', __name__)
controller = TaskController()


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(controller.get_all()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    return jsonify(controller.get_by_id(task_id)), 200


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    result = controller.create(data)
    return jsonify(result), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    result = controller.update(task_id, data)
    return jsonify(result), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = controller.delete(task_id)
    return jsonify(result), 200


@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    filters = {
        'q': request.args.get('q', ''),
        'status': request.args.get('status', ''),
        'priority': request.args.get('priority', ''),
        'user_id': request.args.get('user_id', ''),
    }
    return jsonify(controller.search(filters)), 200


@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    return jsonify(controller.get_stats()), 200
