import unittest
from unittest import TestCase

from app import create_app
from lsb.forms import EncodeForm


class EncodeFormTest(TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.appcontext = self.app.app_context()
        self.appcontext.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self) -> None:
        self.appcontext.pop()
        self.request_context.pop()
        self.app = None
        self.appcontext = None
        self.request_context = None

    def test_message_label(self):
        with self.appcontext and self.request_context:
            form = EncodeForm()
            self.assertEqual(form.message.label.text, "Message")

    def test_image_label(self):
        with self.appcontext and self.request_context:
            form = EncodeForm()
            self.assertEqual(form.image.label.text, "Image")

    def test_consumed_bits_label(self):
        with self.appcontext and self.request_context:
            form = EncodeForm()
            self.assertEqual(form.consumed_bits.label.text, "How many bits per color channel to be used for encoding?")

    def test_submit_label(self):
        with self.appcontext and self.request_context:
            form = EncodeForm()
            self.assertEqual(form.submit.label.text, "Submit")


if __name__ == '__main__':
    unittest.main()
