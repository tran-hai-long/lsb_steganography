from flask import Blueprint, render_template

bp = Blueprint("lsb", __name__, url_prefix="/lsb")


@bp.route("/")
def index():
    return render_template("index.html")
