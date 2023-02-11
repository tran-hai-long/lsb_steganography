from flask import Blueprint, render_template

from app.forms import EncodeForm, DecodeForm

bp = Blueprint("lsb", __name__, url_prefix="/lsb")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/encode/")
def encode():
    form = EncodeForm()
    return render_template("encode.html", form=form)


@bp.route("/decode/")
def decode():
    form = DecodeForm()
    return render_template("decode.html", form=form)
