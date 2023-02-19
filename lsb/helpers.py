import base64
from io import BytesIO

from PIL import Image
from filetype import filetype

from lsb.bin_ascii import bin_to_ascii_str
from lsb.views import DELIMITER_LENGTH, BIN_DELIMITER, BIN_DELIMITER_LENGTH, STARTER_LENGTH, BIN_STARTER, \
    BIN_STARTER_LENGTH


def verify_png(file):
    return filetype.guess(file).mime == "image/png"


def verify_ascii(message):
    for char in message:
        if ord(char) >= 128:
            return False
    return True


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


# Convert the color to a binary string, then to a list of binary numbers.
# Replace bit at the desired position, then convert it back to int.
def merge_lsb(color, msg_bit, bit_position):
    binary_color: list = list(format(color, "08b"))
    binary_color[-1 - bit_position] = msg_bit
    return int("".join(binary_color), 2)


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


def decode(image, consumed_bits):
    pixel_list: list = list(image.getdata())
    bin_msg_with_starter_and_delimiter: str = ""
    no_starter = False
    for pixel in pixel_list:
        for color in pixel:
            binary_color: str = format(color, "08b")
            bin_msg_with_starter_and_delimiter += binary_color[-consumed_bits:]
        # quickly check the first few bytes for STARTER to see if it's an encoded image or not.
        if len(bin_msg_with_starter_and_delimiter) == BIN_STARTER_LENGTH:
            if bin_msg_with_starter_and_delimiter != BIN_STARTER:
                no_starter = True
                break
        if bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] == BIN_DELIMITER:
            break
    if (bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] != BIN_DELIMITER) or no_starter:
        return "Error: Either this is not an encoded image, or you picked the wrong number of bit-per-channel."
    result_with_starter_and_delimiter = bin_to_ascii_str(bin_msg_with_starter_and_delimiter)
    return result_with_starter_and_delimiter[STARTER_LENGTH:-DELIMITER_LENGTH]
