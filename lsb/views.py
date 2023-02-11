from flask import render_template

from lsb.forms import EncodeForm, DecodeForm

from flask import Blueprint

bp_lsb = Blueprint("lsb", __name__, url_prefix="/lsb", template_folder="templates")


@bp_lsb.route("/")
def index():
    return render_template("index.html")


@bp_lsb.route("/encode/")
def encode():
    form = EncodeForm()
    return render_template("encode.html", form=form)


@bp_lsb.route("/decode/")
def decode():
    form = DecodeForm()
    return render_template("decode.html", form=form)
