from extension import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class BusinessRegistration(db.Model):
    business_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('users.account_id'), nullable=False)
    business_registration_no = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    official_contact_no = db.Column(db.String(50), nullable=False)
    business_address = db.Column(db.String(255), nullable=False)
    taxpayer_name = db.Column(db.String(255), nullable=False)
    total_employees = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_beds = db.Column(db.Integer, nullable=False)
