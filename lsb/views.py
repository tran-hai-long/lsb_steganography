from PIL import Image
from flask import Blueprint, request
from flask import render_template

from .bin_ascii import ascii_str_to_bin
from .forms import EncodeForm, DecodeForm

bp_lsb = Blueprint(
    "lsb", __name__, url_prefix="/lsb", template_folder="templates", static_folder="static"
)

STARTER: str = "#start#"
STARTER_LENGTH: int = len(STARTER)
BIN_STARTER: str = ascii_str_to_bin(STARTER)
BIN_STARTER_LENGTH: int = len(BIN_STARTER)
DELIMITER: str = "#end#"
DELIMITER_LENGTH: int = len(DELIMITER)
BIN_DELIMITER: str = ascii_str_to_bin(DELIMITER)
BIN_DELIMITER_LENGTH: int = len(BIN_DELIMITER)

# move this import down to avoid circular import
from lsb.helpers import (
    verify_png,
    verify_ascii,
    verify_channel,
    check_if_msg_fit_in_img,
    encode,
    decode,
    verify_png_jpeg,
    buffer_and_convert_b64,
)


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
    if not verify_png_jpeg(form.image.data):
        return render_template("encode.html", form=form, error="PNG images only.")
    # Delimiter is used to signal the end of message
    msg_with_starter_and_delimiter: str = STARTER + form.message.data + DELIMITER
    bin_msg_with_starter_and_delimiter: str = ascii_str_to_bin(msg_with_starter_and_delimiter)
    consumed_bits: int = int(form.consumed_bits.data)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("encode.html", form=form, error="RGB or RGBA color channel only.")
    if not check_if_msg_fit_in_img(
        bin_msg_with_starter_and_delimiter, image, channel, consumed_bits
    ):
        return render_template(
            "encode.html", form=form, error="The message does not fit in the image."
        )
    result: Image = encode(bin_msg_with_starter_and_delimiter, image, consumed_bits)
    # Pillow Image objects can not be displayed in HTML, thus it is necessary to convert it to base64
    result_base64: str = buffer_and_convert_b64(result)
    return render_template("encode.html", form=form, result=result_base64)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("decode.html", form=form)
    if not verify_png(form.image.data):
        return render_template("decode.html", form=form, error="PNG images only.")
    consumed_bits: int = int(form.consumed_bits.data)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("decode.html", form=form, error="RGB or RGBA color channel only.")
    result: str = decode(image, consumed_bits)
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
