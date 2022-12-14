from pathlib import Path

basedir = Path(__file__).parent.parent


class Baseconfig:
    SECRET_KEY = "Hvtqyqf2UZRx2SDPsupr"
    WTF_CSRF_SECRET_KEY = "PhtsHtVr8kdqByxfSr3v"
    UPLOAD_FOLDER = str(Path(basedir, "apps", "images"))


class LocalConfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir/ 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class TestingConfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False


config = {"testing": TestingConfig, "local": LocalConfig}
