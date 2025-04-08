import os
from app import create_app, db
from app.models.user import User
from app.models.task import Task
import sqlalchemy

# Set up database URI
db_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'app.db')

# Create app with config
app = create_app()

# Update configuration
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create all tables
with app.app_context():
    print("Creating database tables...")
    
    # Drop existing tables if they exist
    db.metadata.drop_all(bind=db.engine)
    
    # Create tables
    db.metadata.create_all(bind=db.engine)
    print("Database tables created successfully!")
    
    # Verify tables exist
    print("\nTables in database:")
    inspector = sqlalchemy.inspect(db.engine)
    print(inspector.get_table_names())
    
    # Try creating a test user
    try:
        test_user = User(username='testuser', email='test@example.com', password='password123')
        db.session.add(test_user)
        db.session.commit()
        print("\nSuccessfully created test user!")
        print("Test user details:", test_user.to_dict())
    except Exception as e:
        print(f"\nError creating test user: {str(e)}")
