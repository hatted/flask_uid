from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response
from app import db
from models import User
import random
import csv
import io
import re

admin_bp = Blueprint('admin', __name__)

# Admin credentials
ADMIN_USERNAME = 'raymond.tsang'
ADMIN_PASSWORD = 'Academy!234'

def validate_uid(uid):
    """Validate that UID is a number with at least 8 digits"""
    if not uid.isdigit():
        return False, "UID must contain only numbers"
    if len(uid) < 8:
        return False, "UID must be at least 8 digits long"
    return True, ""

def generate_captcha():
    """Generate a simple math captcha"""
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return num1, num2, num1 + num2

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        captcha_answer = request.form.get('captcha_answer', '')
        captcha_expected = session.get('captcha_answer')
        
        # Validate captcha first
        try:
            if int(captcha_answer) != captcha_expected:
                flash('Invalid captcha! Please try again.', 'error')
                # Generate new captcha for retry
                num1, num2, answer = generate_captcha()
                session['captcha_answer'] = answer
                return render_template('admin/login.html', captcha_num1=num1, captcha_num2=num2)
        except (ValueError, TypeError):
            flash('Please enter a valid number for captcha.', 'error')
            # Generate new captcha for retry
            num1, num2, answer = generate_captcha()
            session['captcha_answer'] = answer
            return render_template('admin/login.html', captcha_num1=num1, captcha_num2=num2)
        
        # Validate credentials
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session.pop('captcha_answer', None)  # Clear captcha from session
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials!', 'error')
            # Generate new captcha for retry
            num1, num2, answer = generate_captcha()
            session['captcha_answer'] = answer
            return render_template('admin/login.html', captcha_num1=num1, captcha_num2=num2)
    
    # Generate captcha for GET request
    num1, num2, answer = generate_captcha()
    session['captcha_answer'] = answer
    return render_template('admin/login.html', captcha_num1=num1, captcha_num2=num2)

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        flash('Please login to access admin panel.', 'error')
        return redirect(url_for('admin.login'))
    
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if not session.get('admin_logged_in'):
        flash('Please login to access admin panel.', 'error')
        return redirect(url_for('admin.login'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid'].strip()
        email = request.form['email']
        
        # Validate UID format
        is_valid, error_message = validate_uid(uid)
        if not is_valid:
            flash(error_message, 'error')
            return render_template('admin/edit_user.html', user=user)
        
        # Check if UID already exists for other users
        existing_user = User.query.filter(User.uid == uid, User.id != user_id).first()
        if existing_user:
            flash('UID already exists. Please use a different UID.', 'error')
            return render_template('admin/edit_user.html', user=user)
        
        # Update user
        user.name = name
        user.uid = uid
        user.email = email
        
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        flash('Please login to access admin panel.', 'error')
        return redirect(url_for('admin.login'))
    
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user.name}" deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the user.', 'error')
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/export')
def export_csv():
    if not session.get('admin_logged_in'):
        flash('Please login to access admin panel.', 'error')
        return redirect(url_for('admin.login'))
    
    users = User.query.all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Name', 'User ID', 'Email'])
    
    # Write user data
    for user in users:
        writer.writerow([user.id, user.name, user.uid, user.email])
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=users_export.csv'
    
    return response

@admin_bp.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))