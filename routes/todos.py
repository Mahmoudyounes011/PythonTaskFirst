from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.todo import Todo

todos = Blueprint('todos', __name__)

@todos.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    
    required_fields = ['title']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': 'Title is required'
        }), 400
    
    try:
        new_todo = Todo.create({
            'title': data['title'],
            'description': data.get('description', ''),
            'completed': data.get('completed', False),
            'user_id': get_jwt_identity()
        })
        return jsonify({
            'status': 'success',
            'data': {
                'id': new_todo['id'],
                'title': new_todo['title'],
                'completed': new_todo['completed']
            }
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@todos.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    try:
        user_id = get_jwt_identity()
        todos = Todo.get_by_user(user_id)
        return jsonify({
            'status': 'success',
            'count': len(todos),
            'data': todos
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@todos.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        updated_count = Todo.update(
            todo_id=todo_id,
            user_id=user_id,
            data={
                'title': data.get('title'),
                'description': data.get('description'),
                'completed': data.get('completed')
            }
        )
        
        if updated_count == 0:
            return jsonify({
                'status': 'error',
                'message': 'Todo not found or not authorized'
            }), 404
            
        return jsonify({
            'status': 'success',
            'message': 'Todo updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500