from flask import Flask, redirect, request
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

import config
from lsb import views


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    csp = {"default-src": "'self'", "img-src": ["'self'", "data:"]}
    Talisman(app, content_security_policy=csp)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(views.bp_lsb)

    @app.route("/")
    def index_redirect():
        return redirect("/lsb/")

    @app.before_request
    def verify_host():
        if request.host not in config.DevConfig.ALLOWED_HOSTS:
            return "Unable to process hostname", 421

    return app
