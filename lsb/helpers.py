import base64
from io import BytesIO

from PIL import Image
from filetype import filetype

from lsb.bin_ascii import bin_to_ascii_str
from lsb.views import (
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
def merge_lsb(color: int, msg_bit: str, bit_position: int):
    binary_color: list = list(format(color, "08b"))
    binary_color[-bit_position] = msg_bit
    return int("".join(binary_color), 2)


def encode(bin_msg: str, image: Image, consumed_bits: int):
    pixel_list: list = list(image.getdata())
    bin_msg_index: int = 0
    pixel_count: int = 0
    done: bool = False
    for pixel in pixel_list:
        # getdata() returns a list of tuples. Since tuples are immutable, it is necessary to
        # convert them to list.
        pixel: list = list(pixel)
        color_channel: int = 0
        for color in pixel:
            for bit_count in range(consumed_bits, 0, -1):
                if bin_msg_index < len(bin_msg):
                    pixel[color_channel] = merge_lsb(
                        pixel[color_channel], bin_msg[bin_msg_index], bit_count
                    )
                    bin_msg_index += 1
                else:
                    done = True
            color_channel += 1
            if done:
                break
        pixel: tuple = tuple(pixel)
        pixel_list[pixel_count] = pixel
        pixel_count += 1
        if done:
            break
    result: Image = Image.new(mode=image.mode, size=(image.width, image.height))
    result.putdata(pixel_list)
    return result


def extract_lsb(color: int, bit_position: int):
    binary_color: str = format(color, "08b")
    return binary_color[-bit_position]


def decode(image: Image, consumed_bits: int):
    pixel_list: list = list(image.getdata())
    bin_msg_with_starter_and_delimiter: str = ""
    no_starter: bool = False
    done: bool = False
    for pixel in pixel_list:
        for color in pixel:
            for bit_position in range(consumed_bits, 0, -1):
                bin_msg_with_starter_and_delimiter += extract_lsb(color, bit_position)
                # quickly check the first few bytes for STARTER to see if it's an encoded image or not.
                if len(bin_msg_with_starter_and_delimiter) == BIN_STARTER_LENGTH:
                    if bin_msg_with_starter_and_delimiter != BIN_STARTER:
                        no_starter = True
                        break
                # Stop the loop when delimiter is found
                if bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] == BIN_DELIMITER:
                    done = True
            if done or no_starter:
                break
        if done or no_starter:
            break
    # Return an error if starter is not found, or starter is found but delimiter is not found
    if (bin_msg_with_starter_and_delimiter[-BIN_DELIMITER_LENGTH:] != BIN_DELIMITER) or no_starter:
        return "Error: Either this is not an encoded image, or you picked the wrong number of bit-per-channel."
    result_with_starter_and_delimiter = bin_to_ascii_str(bin_msg_with_starter_and_delimiter)
    return result_with_starter_and_delimiter[STARTER_LENGTH:-DELIMITER_LENGTH]


def buffer_and_convert_b64(image: Image):
    image_buffer: BytesIO = BytesIO()
    image.save(image_buffer, format="PNG")
    image_base64: str = base64.b64encode(image_buffer.getvalue()).decode("utf-8")
    return image_base64
