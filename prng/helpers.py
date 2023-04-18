import base64
import itertools
import random
from io import BytesIO

from PIL import Image
from filetype import filetype

from lsb.bin_ascii import bin_to_ascii_str
from .views import (
    DELIMITER_LENGTH,
    BIN_DELIMITER,
    BIN_DELIMITER_LENGTH,
    STARTER_LENGTH,
    BIN_STARTER,
    BIN_STARTER_LENGTH,
)


def verify_png(file):
    return filetype.guess(file).mime == "image/png"


def verify_png_jpeg(file):
    img_type = filetype.guess(file).mime
    return (img_type == "image/png") or (img_type == "image/jpeg")


def verify_ascii(message: str):
    for char in message:
        if ord(char) >= 128:
            return False
    return True


def verify_channel(image: Image):
    match image.mode:
        case "RGB":
            return 3
        case "RGBA":
            return 4
        case _:
            return 0


def check_if_msg_fit_in_img(bin_msg: str, image: Image, channel: int, consumed_bits: int):
    max_size: int = image.width * image.height * channel * consumed_bits
    return len(bin_msg) < max_size


# Convert the color to a binary string, then to a list of binary numbers.
# Replace bit at the desired position, then convert it back to int.
def merge_lsb(color: int, msg_bit: str):
    binary_color: list = list(format(color, "08b"))
    binary_color[-1] = msg_bit
    return int("".join(binary_color), 2)


def encode(bin_msg: str, image: Image, channel: int, seed: str):
    pixel_list: list = list(image.getdata())
    one_dimensional_color_list: list = list(itertools.chain.from_iterable(pixel_list))
    bin_msg_index: int = 0
    random.seed(seed)
    sample = random.sample(range(0, len(one_dimensional_color_list)), len(bin_msg))
    for color_index in sample:
        one_dimensional_color_list[color_index] = merge_lsb(one_dimensional_color_list[color_index], bin_msg[bin_msg_index])
        bin_msg_index += 1
    new_pixel_list = [tuple(one_dimensional_color_list[i:i+channel]) for i in range(0, len(one_dimensional_color_list), channel)]
    result: Image = Image.new(mode=image.mode, size=(image.width, image.height))
    result.putdata(new_pixel_list)
    return result


def extract_lsb(color: int):
    binary_color: str = format(color, "08b")
    return binary_color[-1]


def decode(image: Image, seed: str):
    pixel_list: list = list(image.getdata())
    one_dimensional_color_list: list = list(itertools.chain.from_iterable(pixel_list))
    bin_msg_with_starter_and_delimiter: str = ""
    no_starter: bool = False
    random.seed(seed)
    num_of_colors = len(one_dimensional_color_list)
    sample = random.sample(range(0, num_of_colors), (num_of_colors - 1))
    for color_index in sample:
        bin_msg_with_starter_and_delimiter += extract_lsb(one_dimensional_color_list[color_index])
        # quickly check the first few bytes for STARTER to see if it's an encoded image or not.
        if len(bin_msg_with_starter_and_delimiter) == BIN_STARTER_LENGTH:
            if bin_msg_with_starter_and_delimiter != BIN_STARTER:
                no_starter = True
                break
                # Stop the loop when delimiter is found
        if bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] == BIN_DELIMITER:
            break
    # Return an error if starter is not found, or starter is found but delimiter is not found
    if no_starter:
        return "Error: Either this is not an encoded image, or you entered the wrong seed."
    if (bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] != BIN_DELIMITER):
        return "Error: Starter found, but delimiter is not found."
    result_with_starter_and_delimiter = bin_to_ascii_str(bin_msg_with_starter_and_delimiter)
    return result_with_starter_and_delimiter[STARTER_LENGTH:-DELIMITER_LENGTH]


def buffer_and_convert_b64(image: Image):
    image_buffer: BytesIO = BytesIO()
    image.save(image_buffer, format="PNG")
    image_base64: str = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
    return image_base64
