import os


class DevConfig:
    SECRET_KEY = "dev"
    ALLOWED_HOSTS = ["127.0.0.1:5000"]


class ProdConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    ALLOWED_HOSTS = os.environ.get("FLASK_ALLOWED_HOSTS")
