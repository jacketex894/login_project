import unittest
from datetime import datetime

from lib.Token import Token, JWTToken


class TestToken(unittest.TestCase):
    def setUp(self):
        self.token_handler = Token(JWTToken())
        self.data = {
            "user_name": "test_user",
        }

    def test_generate_token(self):
        token = self.token_handler.encode(self.data)
        decode_data = self.token_handler.decode(token)
        self.assertEqual(decode_data["user_name"], self.data["user_name"])
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())


if __name__ == "__main__":
    unittest.main()
