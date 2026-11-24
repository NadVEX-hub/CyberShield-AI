import unittest
from predict import predict_url


class SecurityTests(unittest.TestCase):

    def test_empty_url(self):
        with self.assertRaises(ValueError):
            predict_url("")

    def test_invalid_url(self):
        with self.assertRaises(ValueError):
            predict_url("hello123")

    def test_invalid_protocol(self):
        with self.assertRaises(ValueError):
            predict_url("ftp://example.com")

    def test_long_url(self):
        with self.assertRaises(ValueError):
            predict_url("https://example.com/" + "a" * 5000)

    def test_url_with_spaces(self):
        with self.assertRaises(ValueError):
            predict_url("https://example .com")

    def test_missing_hostname(self):
        with self.assertRaises(ValueError):
            predict_url("https://")

    def test_valid_url(self):
        prediction, risk = predict_url("https://example.com")

        self.assertIn(prediction, [0, 1])
        self.assertTrue(0 <= risk <= 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
