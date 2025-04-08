"""
User model module for the Task Management API.

This module defines the User model and related functionality for user authentication and authorization.
"""

from datetime import datetime
import bcrypt
from app import db

class User(db.Model):
    """
    User model for authentication and authorization.

    Represents a user in the system who can create and manage tasks.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def __init__(self, username, email, password, role='user'):
        """
        Initialize a new User instance.

        Args:
            username (str): User's username (must be unique)
            email (str): User's email address (must be unique)
            password (str): User's password (will be hashed)
            role (str): User's role ('user' or 'admin'). Defaults to 'user'.
        """
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        """
        Hash and set the user's password.

        Args:
            password (str): Plain text password to hash
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def check_password(self, password):
        """
        Verify a password against the stored hash.

        Args:
            password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """
        Convert User object to a dictionary representation.

        Returns:
            dict: Dictionary containing user information
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
