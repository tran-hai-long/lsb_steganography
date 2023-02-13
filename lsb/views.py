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
    if request.method != "POST" or not form.validate_on_submit():
        return render_template("encode.html", form=form)
    if not verify_ascii(form.message.data):
        return render_template("encode.html", form=form, error="ASCII characters only.")
    if not verify_png(form.image.data):
        return render_template("encode.html", form=form, error="PNG images only.")
    msg_with_delimiter: str = form.message.data + "#end#"
    bin_msg_with_delimiter: str = ascii_str_to_bin(msg_with_delimiter)
    image: Image = Image.open(form.image.data)
    channel: int = verify_channel(image)
    if not channel:
        return render_template("encode.html", form=form, error="RGB or RGBA color channel only.")
    if not check_if_msg_fit_in_img(bin_msg_with_delimiter, image, channel):
        return render_template("encode.html", form=form, error="The message does not fit in the image.")
    encode(bin_msg_with_delimiter, image, channel)  # encode() will return "result" Image to be used in the next line.
    return render_template("encode.html", form=form, result=None)


@bp_lsb.route("/decode/", methods=["GET", "POST"])
def decode_page():
    form = DecodeForm()
    error: str = ""
    if request.method == "POST" and form.validate_on_submit():
        if verify_png(form.image.data):
            decode(form.image.data)
        else:
            error = "Invalid image."
    return render_template("decode.html", form=form, error=error)


def verify_png(file):
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
