import unittest
import logging
from datetime import datetime

from controller.user_profile import (
    UsernamePasswordUserProfile,
    RegisterRequest,
    LoginRequest,
)
from model.user_database import UserDatabase
from model.error import LoginWithWrongPasswordError

logging.getLogger().addHandler(logging.NullHandler())


class TestUserProfile(unittest.TestCase):
    """
    Test case for user register and login.
    """

    def setUp(self):
        self.register_data: RegisterRequest = {
            "user_name": "test_user",
            "password": "test_password",
            "mail": "test_mail@example.com",
        }
        self.login_data: LoginRequest = {
            "user_name": "test_user",
            "password": "test_password",
        }
        self.wrong_data: LoginRequest = {
            "user_name": "test_user",
            "password": "test_wrong",
        }
        self.ip = "127.0.0.1"

    def tearDown(self):
        user_database = UserDatabase()
        delete_user = user_database.query(self.register_data["user_name"])
        user_database.delete(delete_user.user_id)

    def test_user_register(self):
        """
        Test user register and register with duplicate information.
        """
        user_profile_handler = UsernamePasswordUserProfile()
        content = user_profile_handler.register(self.register_data)
        self.assertEqual(content["message"], "User successfully registered")
        self.assertEqual(content["user_name"], self.register_data["user_name"])

    def test_user_login(self):
        """
        Test user login and store JWT in cookie.
        """
        user_profile_handler = UsernamePasswordUserProfile()
        user_profile_handler.register(self.register_data)

        content, token = user_profile_handler.login(self.login_data, self.ip)
        self.assertEqual(content["message"], "Login success")
        decode_data = user_profile_handler.token_handler.decode(token)
        user_database = UserDatabase()
        retrieved_user = user_database.query(self.register_data["user_name"])
        self.assertEqual(int(decode_data["sub"]), retrieved_user.user_id)
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())

        with self.assertRaises(LoginWithWrongPasswordError):
            user_profile_handler.login(self.wrong_data, self.ip)


if __name__ == "__main__":
    unittest.main()
