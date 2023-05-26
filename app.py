from flask import Flask, request, render_template
from flask_talisman import Talisman
from flask_wtf import CSRFProtect

import config
from lsb.views import bp_lsb
from prng.views import bp_prng


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    csp = {"default-src": "'self'", "img-src": ["'self'", "data:"], 'script-src': 'unpkg.com'}
    Talisman(app, content_security_policy=csp)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.register_blueprint(bp_lsb)
    app.register_blueprint(bp_prng)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/tou/")
    def terms_of_use_page():
        return render_template("tou.html")

    @app.route("/privacy/")
    def privacy_policy_page():
        return render_template("privacy.html")

    @app.route("/about/")
    def about_page():
        return render_template("about.html")

    @app.before_request
    def verify_host():
        if request.host not in config.DevConfig.ALLOWED_HOSTS:
            return "Unable to process hostname", 421

    return app
