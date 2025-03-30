# Authentication controller
# Handles user registration, login and logout
# Still need to add form validation - note to self

from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from models import db, User
from datetime import datetime

# Create blueprint
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Store user info in session
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            
            # Redirect based on role
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        else:
            # Really wish Flask had better error handling built in
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        qualification = request.form.get('qualification')
        dob_str = request.form.get('dob')
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('auth/register.html')
        
        # Parse date of birth
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date() if dob_str else None
        except ValueError:
            flash('Invalid date format for Date of Birth', 'danger')
            return render_template('auth/register.html')
        
        # Create new user
        new_user = User(
            username=username,
            full_name=full_name,
            qualification=qualification,
            dob=dob
        )
        new_user.set_password(password)
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth.route('/logout')
def logout():
    """Handle user logout"""
    # Clear session data
    session.pop('user_id', None)
    session.pop('is_admin', None)
    flash('You have been logged out', 'success')
    return redirect(url_for('index'))