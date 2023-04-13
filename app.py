from flask import Flask, redirect, request
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

import config
from lsb.views import bp_lsb
from prng.views import bp_prng


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    csp = {"default-src": "'self'", "img-src": ["'self'", "data:"]}
    Talisman(app, content_security_policy=csp)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(bp_lsb)
    app.register_blueprint(bp_prng)

    @app.route("/")
    def index_redirect():
        return redirect("/lsb/")

    @app.before_request
    def verify_host():
        if request.host not in config.DevConfig.ALLOWED_HOSTS:
            return "Unable to process hostname", 421

    return app
