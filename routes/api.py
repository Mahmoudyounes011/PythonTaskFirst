from flask import Blueprint, request, jsonify
from models.student import Student
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

@api.route('/students', methods=['POST'])
@jwt_required()
def create_student():
    data = request.get_json()
    
    required_fields = ['first_name', 'last_name', 'age', 'specialization']
    if not all(field in data for field in required_fields):
        return jsonify({
            'status': 'error',
            'message': 'Missing required fields'
        }), 400
    
    if not isinstance(data['age'], int):
        return jsonify({
            'status': 'error',
            'message': 'Age must be an integer'
        }), 400
    
    try:
        new_student = Student.create(data)
        return jsonify({
            'status': 'success',
            'data': new_student
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@api.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    try:
        students = Student.get_all()
        return jsonify({
            'status': 'success',
            'count': len(students),
            'data': students
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    try:
        student = Student.get_by_id(student_id)
        return jsonify({
            'status': 'success',
            'data': student
        })
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