import os

from flask import Flask, redirect

from . import lsb


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "dev"),
    )

    app.register_blueprint(lsb.bp)

    # a simple page that says hello
    @app.route("/")
    def hello():
        return redirect("/lsb/")

    return app
