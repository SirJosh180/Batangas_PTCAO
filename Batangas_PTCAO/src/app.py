from flask import Flask, render_template, request, redirect, url_for, session, flash
from extension import db
from model import User

app = Flask(__name__, template_folder='routes', static_folder='static')
app.config.from_object('config.Config')
app.secret_key = "SECRET_KEY"
db.init_app(app)


@app.route('/')
def home():
    return render_template('Login.html')


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


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)