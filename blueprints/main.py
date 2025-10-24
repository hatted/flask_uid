from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import User
import re

main_bp = Blueprint('main', __name__)

def validate_uid(uid):
    """Validate that UID is a number with at least 8 digits"""
    if not uid.isdigit():
        return False, "UID must contain only numbers"
    if len(uid) < 8:
        return False, "UID must be at least 8 digits long"
    return True, ""

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid'].strip()
        email = request.form['email']
        
        # Validate UID format
        is_valid, error_message = validate_uid(uid)
        if not is_valid:
            flash(error_message, 'error')
            return render_template('register.html')
        
        # Check if UID already exists
        existing_user = User.query.filter_by(uid=uid).first()
        if existing_user:
            flash('UID already exists. Please use a different UID.', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(name=name, uid=uid, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('register.html')