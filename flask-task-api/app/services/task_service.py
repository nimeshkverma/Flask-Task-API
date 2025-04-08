"""
Task service module for the Task Management API.

This module provides business logic and helper functions for task management operations.
"""

from ..models.task import Task, db
from ..models.user import User
from flask import abort
from http import HTTPStatus

def user_can_access_task(user, task):
    if user.role == 'admin':
        return True
    return task.user_id == user.id

class TaskService:
    """
    Service class for task management operations.

    Provides methods for creating, updating, deleting, and retrieving tasks.
    """
    
    @staticmethod
    def get_all_tasks(user):
        """
        Get all tasks for a given user.

        Args:
            user (User): The user to get tasks for

        Returns:
            list: List of Task objects
        """
        if user.role == 'admin':
            return Task.query.all()
        return Task.query.filter_by(user_id=user.id).all()

    @staticmethod
    def get_task_by_id(task_id, user):
        """
        Get a specific task by ID.

        Args:
            task_id (int): ID of the task to retrieve
            user (User): The user making the request

        Returns:
            Task: The requested Task object

        Raises:
            HTTPException: 404 Not Found if task doesn't exist
            HTTPException: 403 Forbidden if user doesn't have access
        """
        task = Task.query.get_or_404(task_id)
        if not user_can_access_task(user, task):
            abort(HTTPStatus.FORBIDDEN, "Access denied")
        return task

    @staticmethod
    def create_task(data, user):
        """
        Create a new task.

        Args:
            data (dict): Task data containing title, description, etc.
            user (User): The user creating the task

        Returns:
            Task: The newly created Task object
        """
        from datetime import datetime
        
        # Convert due_date string to datetime object if it exists
        due_date = data.get('due_date')
        if due_date:
            due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        
        task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data.get('status', 'pending'),
            due_date=due_date,
            priority=data.get('priority', 1),
            user_id=user.id
        )
        db.session.add(task)
        db.session.commit()
        return task

    @staticmethod
    def update_task(task_id, data, user):
        """
        Update an existing task.

        Args:
            task_id (int): ID of the task to update
            data (dict): Task data containing fields to update
            user (User): The user making the request

        Returns:
            Task: The updated Task object

        Raises:
            HTTPException: 404 Not Found if task doesn't exist
            HTTPException: 403 Forbidden if user doesn't have access
        """
        task = Task.query.get_or_404(task_id)
        if not user_can_access_task(user, task):
            abort(HTTPStatus.FORBIDDEN, "Access denied")
        
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id, user):
        """
        Delete a task.

        Args:
            task_id (int): ID of the task to delete
            user (User): The user making the request

        Raises:
            HTTPException: 404 Not Found if task doesn't exist
            HTTPException: 403 Forbidden if user doesn't have access
        """
        task = Task.query.get_or_404(task_id)
        if not user_can_access_task(user, task):
            abort(HTTPStatus.FORBIDDEN, "Access denied")
        
        db.session.delete(task)
        db.session.commit()
        return True
