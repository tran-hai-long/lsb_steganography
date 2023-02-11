from flask import Blueprint, request
from flask import render_template

from lsb.forms import EncodeForm, DecodeForm

bp_lsb = Blueprint("lsb", __name__, url_prefix="/lsb", template_folder="templates")


@bp_lsb.route("/")
def index():
    return render_template("index.html")


@bp_lsb.route("/encode/", methods=["GET", "POST"])
def encode_page():
    form = EncodeForm()
    if request.method == "POST" and form.validate_on_submit():
        encode(form.message.data, form.image.data)
    return render_template("encode.html", form=form)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    if request.method == "POST" and form.validate_on_submit():
        decode(form.image.data)
    return render_template("decode.html", form=form)


def encode(message, image):
    pass


def decode(image):
    pass
