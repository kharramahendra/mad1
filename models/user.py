# User model - stores information about users and admin
# Really annoyed that it took so long to get the password hashing right

from models import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """User model for storing user related details"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)  # email
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Define relationship with scores - one user can have many scores
    scores = db.relationship('Score', backref='user', lazy=True)
    
    def set_password(self, password):
        """Create hashed password."""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'