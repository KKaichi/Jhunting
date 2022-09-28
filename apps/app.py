import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from apps.config import config

db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = ""


def create_app(config_key):
    app = Flask(__name__)
    app.config.from_object(config[config_key])
    app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
    app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

    db.init_app(app)
    Migrate(app, db)

    csrf.init_app(app)

    login_manager.init_app(app)

    from apps.home import views as home_views

    app.register_blueprint(home_views.home)

    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    from apps.mypage import views as mypage_views

    app.register_blueprint(mypage_views.mypage, url_prefix="/mypage")

    from apps.contact import views as contact_views

    app.register_blueprint(contact_views.contact, url_prefix="/contact")

    from apps.reset_password import views as reset_password_views

    app.register_blueprint(
        reset_password_views.reset_password, url_prefix="/reset_password"
    )

    from apps.account import views as account_views

    app.register_blueprint(account_views.account, url_prefix="/account")

    return app
