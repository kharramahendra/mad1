# Main application file - the entry point of our application
# Created on: March 30, 2025
# This file initializes the Flask application and sets up the database

from flask import Flask, render_template, redirect, url_for
from controllers.auth_controller import auth
from controllers.user_controller import user
from controllers.admin_controller import admin
import os
from models import db

def create_app():
    app = Flask(__name__)
    
    # Configure database - ensure directory exists and is writable
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_dir = os.path.join(base_dir, 'instance')
    
    # Create instance directory if it doesn't exist
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, 'quiz_master.db')
    
    # Configure Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a proper secret key
    
    # Initialize database with app
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)