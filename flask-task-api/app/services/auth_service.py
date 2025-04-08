"""
Authentication service module for the Task Management API.

This module provides helper functions for user authentication and authorization.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from ..models.user import User

def admin_required():
    """
    Decorator to check if the current user is an admin.

    This decorator should be used on routes that require admin privileges.

    Raises:
        HTTPException: 403 Forbidden if user is not an admin
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or user.role != 'admin':
                return jsonify({'message': 'Admin privileges required'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def get_current_user():
    """
    Get the current authenticated user.

    Returns:
        User: The currently authenticated user object
    """
    user_id = get_jwt_identity()
    return User.query.get(user_id)

def user_can_access_task(user, task):
    """
    Check if a user can access a specific task.

    Args:
        user (User): The user object to check
        task (Task): The task object to check access for

    Returns:
        bool: True if user can access the task, False otherwise
    """
    return user.role == 'admin' or task.user_id == user.id
