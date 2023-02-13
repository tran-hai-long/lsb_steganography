# LSB Steganography

Hiding messages inside images using Least Significant Bit (LSB) steganography. Images are processed with Pillow and
served with Flask.

## Setup

1. Clone this repo.
2. Create a venv virtual environment.
3. Open terminal and run `pip install -r requirements.txt` to install dependencies.
4. Run `flask --debug run`

## Features

- Hide and reveal ASCII messages inside PNG images using LSB steganography.

## TODO
- Delete Image object to save memory.
- Support Unicode (UTF-8) characters.
- Implement Pseudo-random number steganography.

## License

Copyright (c) 2023 Tran Hai Long

This project is licensed under [Mozilla Public License 2.0](LICENSE).
