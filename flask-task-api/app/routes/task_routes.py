"""
Task routes module for the Task Management API.

This module defines the API endpoints for task management operations.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.task_service import TaskService
from ..services.auth_service import get_current_user, admin_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

task_bp = Blueprint('task', __name__)
limiter = Limiter(key_func=get_remote_address)

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
@limiter.limit("100/hour")
def get_tasks():
    """
    Get all tasks for the current user.

    This endpoint returns a list of all tasks that belong to the authenticated user.
    Admin users can view all tasks in the system.

    Returns:
        list: List of task dictionaries
        int: HTTP status code 200
    """
    user = get_current_user()
    tasks = TaskService.get_all_tasks(user)
    return jsonify([task.to_dict() for task in tasks])

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
@limiter.limit("100/hour")
def get_task(task_id):
    """
    Get a specific task by ID.

    This endpoint returns a single task by its ID.
    Users can only access their own tasks unless they are admin.

    Args:
        task_id (int): ID of the task to retrieve

    Returns:
        dict: Task information
        int: HTTP status code 200

    Raises:
        HTTPException: 404 Not Found if task doesn't exist
        HTTPException: 403 Forbidden if user doesn't have access
    """
    user = get_current_user()
    task = TaskService.get_task_by_id(task_id, user)
    return jsonify(task.to_dict())

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
@limiter.limit("100/hour")
def create_task():
    """
    Create a new task.

    This endpoint allows users to create a new task.
    Required fields: title
    Optional fields: description, status, priority, due_date

    Returns:
        dict: Created task information
        int: HTTP status code 201
    """
    user = get_current_user()
    data = request.get_json()
    task = TaskService.create_task(data, user)
    return jsonify(task.to_dict()), 201

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("100/hour")
def update_task(task_id):
    """
    Update an existing task.

    This endpoint allows users to update a task's information.
    Users can only update their own tasks unless they are admin.

    Args:
        task_id (int): ID of the task to update

    Returns:
        dict: Updated task information
        int: HTTP status code 200

    Raises:
        HTTPException: 404 Not Found if task doesn't exist
        HTTPException: 403 Forbidden if user doesn't have access
    """
    user = get_current_user()
    data = request.get_json()
    task = TaskService.update_task(task_id, data, user)
    return jsonify(task.to_dict())

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@limiter.limit("100/hour")
def delete_task(task_id):
    """
    Delete a task.

    This endpoint allows users to delete a task.
    Users can only delete their own tasks unless they are admin.

    Args:
        task_id (int): ID of the task to delete

    Returns:
        None
        int: HTTP status code 204

    Raises:
        HTTPException: 404 Not Found if task doesn't exist
        HTTPException: 403 Forbidden if user doesn't have access
    """
    user = get_current_user()
    TaskService.delete_task(task_id, user)
    return '', 204

@task_bp.route('/admin/tasks', methods=['GET'])
@jwt_required()
@admin_required()
@limiter.limit("100/hour")
def get_all_tasks_admin():
    """
    Get all tasks (admin only).

    This endpoint returns a list of all tasks in the system.
    Only accessible by admin users.

    Returns:
        list: List of all task dictionaries
        int: HTTP status code 200

    Raises:
        HTTPException: 403 Forbidden if user is not admin
    """
    tasks = TaskService.get_all_tasks(get_current_user())
    return jsonify([task.to_dict() for task in tasks])
