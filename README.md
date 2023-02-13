# LSB Steganography

Hiding messages inside images using Least Significant Bit (LSB) steganography. Images are processed with Pillow and
served with Flask.

## Setup

1. Clone this repo.
2. Create a venv virtual environment.
3. Open terminal and run `pip install -r requirements.txt` to install dependencies.
4. Run `flask --debug run` to start the server.

## Features

- Hide and reveal ASCII messages inside PNG images using LSB steganography.

## TODO

- Add some CSS to make the website look better.
- Allow user to choose the number of LSBs used for encoding and decoding.
- Delete Image object to save memory.
- Support Unicode (UTF-8) characters.
- (Nice to have) Implement Pseudo-random number steganography.

## License

Copyright (c) 2023 Tran Hai Long

This project is licensed under [Mozilla Public License 2.0](LICENSE).
