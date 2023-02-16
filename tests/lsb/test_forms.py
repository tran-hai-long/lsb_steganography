import unittest
from unittest import TestCase

from app import create_app
from lsb.forms import EncodeForm, DecodeForm


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

    def test_message_validator(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            form.message.data = ""
            self.assertFalse(form.message.validate(EncodeForm))
            form.message.data = None
            self.assertFalse(form.message.validate(EncodeForm))

    def test_image_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.image.label.text, "Image")

    def test_image_validator(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            form.image.data = None
            self.assertFalse(form.image.validate(EncodeForm))

    def test_consumed_bits_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.consumed_bits.label.text, "How many bits per color channel to be used for encoding?")

    def test_consumed_bits_choices(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.consumed_bits.choices, [("1", "1bpc"), ("2", "2bpc"), ("4", "4bpc")])

    def test_consumed_bits_validator(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            form.consumed_bits.data = "3"
            self.assertFalse(form.consumed_bits.validate(EncodeForm))
            form.consumed_bits.data = "0"
            self.assertFalse(form.consumed_bits.validate(EncodeForm))

    def test_submit_label(self):
        with self.test_app_context and self.test_request_context:
            form = EncodeForm()
            self.assertEqual(form.submit.label.text, "Submit")


class DecodeFormTest(TestCase):
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

    def test_image_label(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            self.assertEqual(form.image.label.text, "Image")

    def test_image_validator(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            form.image.data = None
            self.assertFalse(form.image.validate(DecodeForm))

    def test_consumed_bits_label(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            self.assertEqual(
                form.consumed_bits.label.text, "How many bits per color channel were used during the encoding process?"
            )

    def test_consumed_bits_choices(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            self.assertEqual(form.consumed_bits.choices, [("1", "1bpc"), ("2", "2bpc"), ("4", "4bpc")])

    def test_consumed_bits_validator(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            form.consumed_bits.data = "3"
            self.assertFalse(form.consumed_bits.validate(DecodeForm))
            form.consumed_bits.data = "0"
            self.assertFalse(form.consumed_bits.validate(DecodeForm))

    def test_submit_label(self):
        with self.test_app_context and self.test_request_context:
            form = DecodeForm()
            self.assertEqual(form.submit.label.text, "Submit")


if __name__ == "__main__":
    unittest.main()
