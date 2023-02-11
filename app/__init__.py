import os

from flask import Flask, redirect
from flask_wtf import CSRFProtect

from . import lsb


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev"),
    )
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(lsb.bp)

    @app.route("/")
    def index_redirect():
        return redirect("/lsb/")

    return app
