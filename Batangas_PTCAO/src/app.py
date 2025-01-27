import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from Batangas_PTCAO.src.extension import db
from Batangas_PTCAO.src.model import User, BusinessRegistration
from Batangas_PTCAO.src.config import Config

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from enum import Enum

class AccountStatus(Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    MAINTENANCE = 'maintenance'

app = Flask(__name__, template_folder='routes', static_folder='static')
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key')

jwt = JWTManager(app)
db.init_app(app)

@app.route('/')
def home():
    return render_template('Login.html')

# needs test case for incorrect password input
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Server-side input validation
        user_email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not user_email or not password:
            flash('Email and password are required', 'error')
            return render_template('Login.html')

        user = User.query.filter_by(user_email=user_email).first()

        if not user:
            flash('User not found', 'error')
            return render_template('Login.html')

        if user.account_status == AccountStatus.SUSPENDED:
            flash('Account is suspended. Contact support.', 'error')
            return render_template('Login.html')

        if user.account_status == AccountStatus.MAINTENANCE:
            flash('System under maintenance', 'error')
            return render_template('Login.html')

        if user.check_password(password):
            # Reset failed attempts
            user.failed_login_attempts = 0
            db.session.commit()

            # Generate JWT token
            access_token = create_access_token(identity=user.user_id)
            session['access_token'] = access_token
            session['account_id'] = user.user_id

            return redirect(url_for('dashboard'))
        else:
            # Increment failed login attempts
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.account_status = AccountStatus.SUSPENDED
                db.session.commit()
                flash('Too many failed attempts. Account locked.', 'error')
                return render_template('Login.html')

            db.session.commit()
            flash('Invalid email or password', 'error')
            return render_template('Login.html')

    return render_template('Login.html')
# Ready for testing
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('Registration.html')

        # Changed from "user" to work with "users" table
        existing_user = User.query.filter_by(user_email=user_email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return render_template('Registration.html')

        new_user = User(user_email=user_email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful', 'success')
        return redirect(url_for('login'))

    return render_template('Registration.html')

@app.route('/business_registration', methods=['GET', 'POST'])
def business_registration():
    if 'account_id' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Collect business registration details
        business_reg_data = {
            'account_id': session['account_id'],
            'business_registration_no': request.form.get('business-registration'),
            'business_name': request.form.get('business-name'),
            'official_contact_no': request.form.get('official-contact'),
            'business_address': request.form.get('business-address'),
            'taxpayer_name': request.form.get('taxpayer-name'),
            'total_employees': request.form.get('total-employees'),
            'total_rooms': request.form.get('total-rooms'),
            'total_beds': request.form.get('total-beds')
        }

        # save business registration
        new_business = BusinessRegistration(**business_reg_data)
        db.session.add(new_business)
        db.session.commit()

        # Redirect to next po
        return redirect(url_for('Special_Service'))

    return render_template('Registration.html')

@app.route('/special_services', methods=['GET', 'POST'])
def special_services():
    if 'account_id' not in session:
        flash('Please log in first', 'error')
        return redirect(url_for('login'))

    business_reg = BusinessRegistration.query.filter_by(account_id=session['account_id']).order_by(BusinessRegistration.business_id.desc()).first()

    if request.method == 'POST':
        return redirect(url_for('LoginCredentials'))

    return render_template('special_services.html', business_reg=business_reg)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    if allowed_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'static'), filename)
    else:
        return 'File type not allowed', 400

def allowed_file(filename):
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)