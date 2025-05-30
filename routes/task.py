from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.task import Task
from models.user import User

task_api = Blueprint('task_api', __name__)

@task_api.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    required_fields = ['title', 'project_id', 'assigned_to', 'due_date']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    try:
        user = User.get_by_id(user_id)

        if not Task.is_project_creator(user['id'], data['project_id']):
            return jsonify({'status': 'error', 'message': 'Only project creator can create tasks'}), 403
        
        task_id = Task.create(data, user)
        return jsonify({'status': 'success', 'task_id': task_id}), 201
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@task_api.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        user = User.get_by_id(user_id)
        task = Task.get_by_id(task_id)
        if not task:
            return jsonify({'status': 'error', 'message': 'Task not found'}), 404
        
        if user['id'] == task['created_by']:

            updated_task = Task.update(task_id, data, can_update_status=False)
        elif user['id'] == task['assigned_to']:

            if 'status' in data:
                updated_task = Task.update_status(task_id, data['status'])
            else:
                return jsonify({'status': 'error', 'message': 'Assigned user can only update status'}), 403
        else:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

        return jsonify({'status': 'success', 'data': updated_task})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@task_api.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    try:
        user = User.get_by_id(user_id)
        task = Task.get_by_id(task_id)
        if not task:
            return jsonify({'status': 'error', 'message': 'Task not found'}), 404
        
        if user['id'] != task['created_by']:
            return jsonify({'status': 'error', 'message': 'Only project creator can delete task'}), 403
        
        Task.delete(task_id)
        return jsonify({'status': 'success', 'message': 'Task deleted'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@task_api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)

    
    status = request.args.get('status')        
    due_date = request.args.get('due_date')    
    project_id = request.args.get('project_id')
    assigned_to = request.args.get('assigned_to')
    search = request.args.get('search')        

    try:
        if user['is_admin']:
            tasks = Task.filter_tasks(
                status=status,
                due_date=due_date,
                project_id=project_id,
                assigned_to=assigned_to,
                search=search
            )
        else:
            tasks = Task.filter_tasks(
                status=status,
                due_date=due_date,
                project_id=project_id,
                assigned_to=user_id,
                search=search,
                user_id=user_id
            )

        return jsonify({'status': 'success', 'count': len(tasks), 'data': tasks})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@task_api.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    try:
        task = Task.get_by_id(task_id)
        if not task:
            return jsonify({'status': 'error', 'message': 'Task not found'}), 404
        
        if user['is_admin'] or user['id'] in [task['created_by'], task['assigned_to']]:
            return jsonify({'status': 'success', 'data': task})
        else:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
