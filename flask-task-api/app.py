"""
Main application file for the Flask Task Management API.

This module initializes the Flask application and provides the entry point for the API.
"""

from app import create_app

app = create_app()

# Create tables
with app.app_context():
    from app import db
    from app.models import user, task
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
