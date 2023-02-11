from filetype import filetype
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
    error = None
    if request.method == "POST" and form.validate_on_submit():
        if verify_image(form.image.data):
            encode(form.message.data, form.image.data)
        else:
            error = "Invalid image."
    return render_template("encode.html", form=form, error=error)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    error = None
    if request.method == "POST" and form.validate_on_submit():
        if verify_image(form.image.data):
            decode(form.image.data)
        else:
            error = "Invalid image."
    return render_template("decode.html", form=form, error=error)


def verify_image(image):
    img_type = filetype.guess(image).mime
    return (img_type == "image/jpeg") or (img_type == "image/png")


def encode(message, image):
    pass


def decode(image):
    pass
