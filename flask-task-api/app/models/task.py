"""
Task model module for the Task Management API.

This module defines the Task model and related functionality for task management.
"""

from datetime import datetime
from app import db

class Task(db.Model):
    """
    Task model for task management.

    Represents a task that can be assigned to a user with various attributes.
    """
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'in_progress', 'completed'
    priority = db.Column(db.String(20), nullable=False, default='medium')  # 'low', 'medium', 'high'
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        """
        Convert Task object to a dictionary representation.

        Returns:
            dict: Dictionary containing task information
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id
        }
