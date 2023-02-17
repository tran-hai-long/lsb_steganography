import unittest
from unittest import TestCase

from app import create_app


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app()
        self.test_app.config["TESTING"] = True
        self.test_client = self.test_app.test_client()

    def tearDown(self) -> None:
        self.test_app = None

    def test_index_page_redirect(self):
        response = self.test_client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_lsb_page_routing(self):
        response = self.test_client.get("/lsb/", follow_redirects=True)
        assert "<title>Index</title>" in response.text


class EncodeViewTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app()
        self.test_app.config["TESTING"] = True
        self.test_client = self.test_app.test_client()

    def tearDown(self) -> None:
        self.test_app = None

    def test_encode_page_routing(self):
        response = self.test_client.get("/lsb/encode/", follow_redirects=True)
        assert "<title>Encode</title>" in response.text


class DecodeViewTest(TestCase):
    def setUp(self) -> None:
        self.test_app = create_app()
        self.test_app.config["TESTING"] = True
        self.test_client = self.test_app.test_client()

    def tearDown(self) -> None:
        self.test_app = None

    def test_decode_page_routing(self):
        response = self.test_client.get("/lsb/decode/", follow_redirects=True)
        assert "<title>Decode</title>" in response.text


if __name__ == "__main__":
    unittest.main()
