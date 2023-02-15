import unittest
from unittest import TestCase

from app import create_app
from lsb.forms import EncodeForm


class EncodeFormTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app()
        self.test_app.config["TESTING"] = True
        self.test_app_context = self.test_app.app_context()
        self.test_app_context.push()
        self.test_request_context = self.test_app.test_request_context()
        self.test_request_context.push()

    def tearDown(self) -> None:
        self.test_app_context.pop()
        self.test_request_context.pop()
        self.test_app = None
        self.test_app_context = None
        self.test_request_context = None

    def test_message_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.message.label.text, "Message")

    def test_image_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.image.label.text, "Image")

    def test_consumed_bits_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.consumed_bits.label.text, "How many bits per color channel to be used for encoding?")

    def test_submit_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.submit.label.text, "Submit")


if __name__ == '__main__':
    unittest.main()
