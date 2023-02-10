from flask import Blueprint, render_template

bp = Blueprint("lsb", __name__, url_prefix="/lsb")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/encode/")
def encode():
    return render_template("encode.html")


@bp.route("/decode/")
def decode():
    return render_template("decode.html")
