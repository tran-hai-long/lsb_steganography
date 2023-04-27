# LSB Steganography

Hiding messages inside images using Least Significant Bit (LSB) or Pseudo-random Number
Generator (PRNG) steganography. Images are processed
by Pillow and served via Flask.

## Installation & Usage

Please see [the Wiki](https://github.com/tran-hai-long/lsb_steganography/wiki).

## Features

- Hide and reveal ASCII messages inside PNG images using Least Significant Bits or
  Pseudo-random Number Generator Steganography.
- Choose the number of bits per byte on the image to be used for the encoding process.
  More bits
  used means you can cramp more data but will result in a drastically changed image.

## TODO

- [x] Allow users to choose the number of LSBs used for encoding and decoding.
- [x] Add some CSS to make the website look better.
- [ ] Support Unicode (UTF-8) characters.
- [x] Implement Pseudo-random number steganography.
- [ ] (Nice to have) AJAX for encode and decode page.

## License

Copyright (c) 2023 Tran Hai Long

This project is licensed under [Mozilla Public License 2.0](LICENSE).
