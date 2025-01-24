from urllib import request
from extension import db
from model import User

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return redirect(url_for('dashboard'))  # Replace with actual route
        else:
            return render_template('Login.html', error='Invalid email or password')
    return render_template('Login.html')

if __name__ == '__main__':
    app.run()