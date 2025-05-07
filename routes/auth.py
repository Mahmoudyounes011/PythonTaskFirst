from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.user import User
from models.revoked_token import RevokedToken
from flask_mail import Message
from utils.emails import send_welcome_email
#from app import mail 

mail = None  # سيتم حقنه من app.py

def init_mail(m):
    global mail
    mail = m
auth_bp = Blueprint('auth', __name__)   

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'address']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        user_id = User.create(data)
        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.find_by_email(email)
    
    if not user or not User.verify_password(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401
    try:
     send_welcome_email(email, mail)  
    except Exception as e:
        print(f"field send email: {e}")

    access_token = create_access_token(identity=user['id'])
    refresh_token = create_refresh_token(identity=user['id'])
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user_id": user['id']
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    RevokedToken.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_token}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        # Get user identity from JWT token
        user_id = get_jwt_identity()
        
        # Fetch user from database
        user = User.get_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Return user info (excluding sensitive data)
        return jsonify({
            "id": user['id'],
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "email": user['email'],
            "phone_number": user['phone_number'],
            "address": user['address'],
            "created_at": user['created_at']
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500