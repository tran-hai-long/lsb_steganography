from PIL import Image
from flask import Blueprint, request
from flask import render_template

from lsb.forms import EncodeForm, DecodeForm
from lsb.helpers import verify_png, verify_ascii, ascii_str_to_bin, verify_channel, check_if_msg_fit_in_img, encode, \
    decode

bp_lsb = Blueprint("lsb", __name__, url_prefix="/lsb", template_folder="templates")


@bp_lsb.route("/")
def index():
    return render_template("index.html")


@bp_lsb.route("/encode/", methods=["GET", "POST"])
def encode_page():
    form = EncodeForm()
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("encode.html", form=form)
    if not verify_ascii(form.message.data):
        return render_template("encode.html", form=form, error="ASCII characters only.")
    if not verify_png(form.image.data):
        return render_template("encode.html", form=form, error="PNG images only.")
    # Delimiter is used to signal the end of message
    msg_with_delimiter: str = form.message.data + "#end#"
    bin_msg_with_delimiter: str = ascii_str_to_bin(msg_with_delimiter)
    consumed_bits: int = int(form.consumed_bits.data)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("encode.html", form=form, error="RGB or RGBA color channel only.")
    if not check_if_msg_fit_in_img(bin_msg_with_delimiter, image, channel, consumed_bits):
        return render_template("encode.html", form=form, error="The message does not fit in the image.")
    # Pillow Image objects can not be displayed in HTML, thus it is necessary to convert it to base64
    result_base64 = encode(bin_msg_with_delimiter, image, consumed_bits)
    return render_template("encode.html", form=form, result=result_base64)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("decode.html", form=form)
    if not verify_png(form.image.data):
        return render_template("decode.html", form=form, error="PNG images only.")
    consumed_bits = int(form.consumed_bits.data)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("decode.html", form=form, error="RGB or RGBA color channel only.")
    result = decode(image, consumed_bits)
    return render_template("decode.html", form=form, result=result)


@bp_lsb.route("/explain/")
def explain_page():
    return render_template("explain.html")


@bp_lsb.route("/tou/")
def terms_of_use_page():
    return render_template("tou.html")


@bp_lsb.route("/privacy/")
def privacy_policy_page():
    return render_template("privacy.html")


@bp_lsb.route("/about/")
def about_page():
    return render_template("about.html")
