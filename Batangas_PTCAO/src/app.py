from functools import wraps
from urllib import request

from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('Login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        pass
