import random, secrets
from PIL import Image
from flask import Blueprint, request
from flask import render_template

from lsb.bin_ascii import ascii_str_to_bin
from .forms import EncodeForm, DecodeForm

bp_prng = Blueprint("prng", __name__, url_prefix="/prng")

STARTER: str = "#start#"
STARTER_LENGTH: int = len(STARTER)
BIN_STARTER: str = ascii_str_to_bin(STARTER)
BIN_STARTER_LENGTH: int = len(BIN_STARTER)
DELIMITER: str = "#end#"
DELIMITER_LENGTH: int = len(DELIMITER)
BIN_DELIMITER: str = ascii_str_to_bin(DELIMITER)
BIN_DELIMITER_LENGTH: int = len(BIN_DELIMITER)

# move this import down to avoid circular import
from .helpers import (
    verify_png,
    verify_ascii,
    verify_channel,
    check_if_msg_fit_in_img,
    encode,
    decode,
    verify_png_jpeg,
    buffer_and_convert_b64,
)


@bp_prng.route("/")
def index():
    return render_template("prng-index.html")


@bp_prng.route("/encode/", methods=["GET", "POST"])
def encode_page():
    form = EncodeForm()
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("prng-encode.html", form=form)
    if not verify_ascii(form.message.data):
        return render_template("prng-encode.html", form=form,
                               error="ASCII characters only.")
    if not verify_png_jpeg(form.image.data):
        return render_template("prng-encode.html", form=form, error="PNG images only.")
    # Delimiter is used to signal the end of message
    msg_with_starter_and_delimiter: str = STARTER + form.message.data + DELIMITER
    bin_msg_with_starter_and_delimiter: str = ascii_str_to_bin(
        msg_with_starter_and_delimiter)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("prng-encode.html", form=form,
                               error="RGB or RGBA color channel only.")
    if not check_if_msg_fit_in_img(
            bin_msg_with_starter_and_delimiter, image, channel, 1
    ):
        return render_template(
            "prng-encode.html", form=form, error="The message does not fit in the image."
        )
    seed: str = secrets.token_hex(32)
    result: Image = encode(bin_msg_with_starter_and_delimiter, image, channel, seed)
    # Pillow Image objects can not be displayed in HTML, thus it is necessary to convert it to base64
    result_base64: str = buffer_and_convert_b64(result)
    return render_template("prng-encode.html", form=form, result=result_base64, seed=seed)


@bp_prng.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("prng-decode.html", form=form)
    if not verify_png(form.image.data):
        return render_template("prng-decode.html", form=form, error="PNG images only.")
    seed: str = form.seed.data
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("prng-decode.html", form=form,
                               error="RGB or RGBA color channel only.")
    result: str = decode(image, seed)
    return render_template("prng-decode.html", form=form, result=result)


@bp_prng.route("/explain/")
def explain_page():
    return render_template("explain.html")


@bp_prng.route("/tou/")
def terms_of_use_page():
    return render_template("tou.html")


@bp_prng.route("/privacy/")
def privacy_policy_page():
    return render_template("privacy.html")


@bp_prng.route("/about/")
def about_page():
    return render_template("about.html")
