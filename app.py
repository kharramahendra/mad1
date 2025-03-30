# Main application file - the entry point of our application
# Created on: March 30, 2025
# This file initializes the Flask application and sets up the database

from flask import Flask, render_template
from models import init_db
import os

# Create the application instance
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-key-should-be-changed-in-production'  # Used for session management

# Initialize the database
init_db(app)

# Import and register blueprints
from controllers.auth_controller import auth
from controllers.admin_controller import admin 
from controllers.user_controller import user

app.register_blueprint(auth)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

@app.route('/')
def index():
    # Spent way too much time fixing this route yesterday, ugh
    return render_template('index.html')

# Run the application if this file is executed directly
if __name__ == '__main__':
    app.run(debug=True)