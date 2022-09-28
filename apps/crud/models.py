import datetime

from apps.app import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )

    def create_token(user_id):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(user_id, salt="kaichi-shio")

    def load_token(token):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.loads(token, salt="kaichi-shio", max_age=600)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_duplicate_email(self):
        return User.query.filter_by(email=self.email).first() is not None


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
