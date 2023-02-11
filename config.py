import os


class DevConfig:
    SECRET_KEY = "dev"


class ProdConfig:
    DEBUG = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
