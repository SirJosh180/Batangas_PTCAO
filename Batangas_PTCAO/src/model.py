from extension import db

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)