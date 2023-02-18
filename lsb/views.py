import base64
from io import BytesIO

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


def verify_png(file):
    return filetype.guess(file).mime == "image/png"


def verify_ascii(message):
    for char in message:
        if ord(char) >= 128:
            return False
    return True


# For each ASCII character, first convert it to Unicode code point form, then format it to binary form.
# Pad 0 to the left if the binary string has less than 8 characters, for consistency.
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


def check_if_msg_fit_in_img(bin_msg, image, channel, consumed_bits):
    max_size: float = image.width * image.height * channel * consumed_bits
    return len(bin_msg) < max_size


def encode(bin_msg, image, consumed_bits):
    pixel_list: list = list(image.getdata())
    bin_msg_index: int = 0
    pixel_count: int = 0
    for pixel in pixel_list:
        pixel: list = list(pixel)
        color_channel: int = 0
        for color in pixel:
            if bin_msg_index < len(bin_msg):
                for bit_count in range(consumed_bits - 1, -1, -1):
                    pixel[color_channel] = merge_lsb(pixel[color_channel], bin_msg[bin_msg_index], bit_count)
                    bin_msg_index += 1
            color_channel += 1
        pixel: tuple = tuple(pixel)
        pixel_list[pixel_count] = pixel
        pixel_count += 1
    result_image = Image.new(mode=image.mode, size=(image.width, image.height))
    result_image.putdata(pixel_list)
    # Keep the image in memory for now, may store it in disk in the future
    buffered = BytesIO()
    result_image.save(buffered, format="PNG")
    result_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return result_base64


# Convert the color to a binary string, then to a list of binary numbers.
# Replace bit at the desired position, then convert it back to int.
def merge_lsb(color, msg_bit, bit_position):
    binary_color: list = list(format(color, "08b"))
    binary_color[-1 - bit_position] = msg_bit
    return int("".join(binary_color), 2)


def decode(image, consumed_bits):
    pixel_list: list = list(image.getdata())
    bin_msg_with_delimiter: str = ""
    for pixel in pixel_list:
        for color in pixel:
            binary_color: str = format(color, "08b")
            bin_msg_with_delimiter += binary_color[-consumed_bits:]
    result = bin_to_ascii_str(bin_msg_with_delimiter)
    return result


def bin_to_ascii_str(bin_msg_with_delimiter):
    bin_index: int = 0
    result_with_delimiter: str = ""
    # Get every 8 character in bin_msg to form a binary number, convert it to Unicode code point number,
    # then convert it to ASCII char
    while (bin_index + 8) < len(bin_msg_with_delimiter):
        char_ord = int(bin_msg_with_delimiter[bin_index: (bin_index + 8)], 2)
        result_with_delimiter += chr(char_ord)
        bin_index += 8
    delimiter_index = result_with_delimiter.find("#end#")
    if delimiter_index == -1:
        return "Either this is not an encoded image, or you picked the wrong number of bit-per-channel."
    return result_with_delimiter[:delimiter_index]


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
