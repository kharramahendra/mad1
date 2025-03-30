# Models package initialization
# Sets up the database and creates initial admin user
# Had to redo this file three times to get relationships right

from flask_sqlalchemy import SQLAlchemy

# Create database instance
db = SQLAlchemy()

# Import models after defining db to avoid circular imports
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.score import Score

def init_db(app):
    """Initialize database and create tables"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables defined in the models
        db.create_all()
        
        # Check if admin exists, if not create one
        # Spent an hour debugging this - make sure admin creation happens in app context
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            admin = User(
                username="admin@quizmaster.com",
                full_name="Admin",
                is_admin=True
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")