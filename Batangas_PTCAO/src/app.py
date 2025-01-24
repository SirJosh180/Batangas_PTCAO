from flask import Flask, render_template, request, redirect, url_for, session, flash
from extension import db
from model import User, BusinessRegistration

app = Flask(__name__, template_folder='routes', static_folder='static')
app.config.from_object('config.Config')
app.secret_key = "SECRET_KEY"
db.init_app(app)


@app.route('/')
def home():
    return render_template('Login.html')

# Run Test - 0
# Working
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(user_email=user_email).first()
        if user and user.check_password(password):
            session['account_id'] = user.user_id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('Login.html')
    return render_template('Login.html')

# Run Test - 0
# Working
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('LoginCredentials.html')

        existing_user = User.query.filter_by(user_email=user_email).first()
        if existing_user:
            flash('Email already exists', 'error')
            return render_template('LoginCredentials.html')

        new_user = User(user_email=user_email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful', 'success')
        return redirect(url_for('login'))

    return render_template('LoginCredentials.html')

# Run Test - 0
# Not yet tested
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
        return redirect(url_for('special_services'))

    return render_template('Registration.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)