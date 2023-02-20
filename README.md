# LSB Steganography

Hiding messages inside images using Least Significant Bit (LSB) steganography. Images are processed by Pillow and
served via Flask.

## Setup

1. Clone this repo.
2. Create a venv virtual environment.
3. Open terminal and run `pip install -r requirements.txt` to install dependencies.
4. Run `flask --debug run` to start the server.

## Features

- Hide and reveal ASCII messages inside PNG images using LSB steganography.
- Choose the number of bits per byte on the image to be used for the encoding process. More bits used means you can
  cramp more data but will result in a drastically changed image.

## TODO

- [x] Allow users to choose the number of LSBs used for encoding and decoding.
- [x] Add some CSS to make the website look better.
- [ ] Support Unicode (UTF-8) characters.
- [ ] Implement Pseudo-random number steganography.
- [ ] (Nice to have) AJAX for encode and decode page.

## License

Copyright (c) 2023 Tran Hai Long

This project is licensed under [Mozilla Public License 2.0](LICENSE).
