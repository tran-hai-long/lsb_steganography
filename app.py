from flask import Flask, redirect
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

from lsb import views


def create_app():
    # create and configure the lsb
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    csp = {
        "default-src": "\'self\'",
        "img-src": ["\'self\'", "data:"]
    }
    Talisman(app, content_security_policy=csp)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(views.bp_lsb)

    @app.route("/")
    def index_redirect():
        return redirect("/lsb/")

    return app
