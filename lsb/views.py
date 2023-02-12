from PIL import Image
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
    error: str = ""
    if request.method == "POST" and form.validate_on_submit():
        if verify_image(form.image.data):
            image: Image = Image.open(form.image.data)
            msg_with_delimiter: str = form.message.data + "#end#"
            if verify_ascii(msg_with_delimiter):
                bin_msg_with_delimiter: str = ascii_str_to_bin(msg_with_delimiter)
                channel: int = verify_channel(image)
                if channel:
                    if check_if_msg_fit_in_img(bin_msg_with_delimiter, image, channel):
                        encode(bin_msg_with_delimiter, image, channel)
                    else:
                        error = "The message does not fit in the image."
                else:
                    error = "Only PNG images with RGB or RGBA color channel are supported."
            else:
                error = "Only ASCII messages are supported."
        else:
            error = "PNG images only."
    return render_template("encode.html", form=form, error=error)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    error: str = ""
    if request.method == "POST" and form.validate_on_submit():
        if verify_image(form.image.data):
            decode(form.image.data)
        else:
            error = "Invalid image."
    return render_template("decode.html", form=form, error=error)


def verify_image(file):
    return filetype.guess(file).mime == "image/png"


def verify_ascii(message):
    for char in message:
        if ord(char) >= 128:
            return False
    return True


def ascii_str_to_bin(string):
    return "".join([format(ord(char), "08b") for char in string])


def verify_channel(image):
    match image.mode:
        case "RGB":
            return 3
        case "RGBA":
            return 4
        case _:
            return 0


def check_if_msg_fit_in_img(bin_msg, image, channel):
    max_size: float = image.width * image.height * channel / 8
    return len(bin_msg) < max_size


def encode(message, image, channel):
    pass


def decode(image):
    pass
