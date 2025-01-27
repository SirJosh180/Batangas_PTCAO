from Batangas_PTCAO.src.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum


class AccountStatus(str, Enum):
    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    MAINTENANCE = 'maintenance'


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    account_status = db.Column(db.String(20), default=AccountStatus.ACTIVE)
    failed_login_attempts = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_suspended(self):
        return self.account_status == AccountStatus.SUSPENDED

    def is_active(self):
        return self.account_status == AccountStatus.ACTIVE

    def update_status(self, new_status):
        if new_status not in AccountStatus:
            raise ValueError("Invalid account status")
        self.account_status = new_status


class BusinessRegistration(db.Model):
    __tablename__ = 'businessregistration'

    business_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    business_registration_no = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(255), nullable=False)
    official_contact_no = db.Column(db.String(50), nullable=False)
    business_address = db.Column(db.String(255), nullable=False)
    taxpayer_name = db.Column(db.String(255), nullable=False)
    total_employees = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_beds = db.Column(db.Integer, nullable=False)