# For each ASCII character, first convert it to Unicode code point form, then format it to binary form.
# Pad 0 to the left if the binary string has less than 8 characters, for consistency.
def ascii_str_to_bin(string: str):
    return "".join([format(ord(char), "08b") for char in string])


# Get every 8 character in bin_msg to form a binary number, convert it to Unicode code point number,
# then convert it to an ASCII char
def bin_to_ascii_str(bin_msg: str):
    bin_index: int = 0
    result: str = ""
    while (bin_index + 8) <= len(bin_msg):
        char_ord = int(bin_msg[bin_index : (bin_index + 8)], 2)
        result += chr(char_ord)
        bin_index += 8
    return result
