from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.project import Project
from models.user import User

project_api = Blueprint('project_api', __name__)

@project_api.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    data = request.get_json()
    try:
        project = Project.create(data, user)
        return jsonify({"status": "success", "data": project}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@project_api.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    try:
        projects = Project.get_all(user)
        return jsonify({"status": "success", "data": projects, "count": len(projects)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@project_api.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    try:
        project = Project.get_by_id(project_id, user)
        return jsonify({"status": "success", "data": project})
    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 403
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@project_api.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    data = request.get_json()
    try:
        updated = Project.update(project_id, data, user)
        return jsonify({"status": "success", "data": updated})
    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 403
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@project_api.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()
    user = User.get_by_id(user_id)
    try:
        Project.delete(project_id, user)
        return jsonify({"status": "success", "message": "Project deleted"})
    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 403
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
