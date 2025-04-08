"""
Authentication routes module for the Task Management API.

This module defines the API endpoints for user authentication and registration.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ..models.user import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    This endpoint allows users to create a new account.

    Returns:
        dict: Success message if registration is successful
        int: HTTP status code 201

    Raises:
        HTTPException: 400 Bad Request if username or email already exists
    """
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
        
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login and get JWT token.

    This endpoint allows users to authenticate and receive a JWT token.

    Returns:
        dict: Access token and user information
        int: HTTP status code 200

    Raises:
        HTTPException: 401 Unauthorized if credentials are invalid
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401
