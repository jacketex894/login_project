import unittest
from fastapi import HTTPException
import logging
from datetime import datetime
from fastapi.responses import JSONResponse
import json

from util.UserProfile import UsernamePasswordUserProfile, RegisterRequest, LoginRequest
from lib.UserDatabase import UserDatabase

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
        response = user_profile_handler.register(self.register_data)
        self.assertIsInstance(response, JSONResponse)

        body = json.loads(response.body.decode("utf-8"))
        self.assertEqual(body["message"], "User successfully registered")
        self.assertEqual(body["user_name"], self.register_data["user_name"])

        # Duplicate Registration
        with self.assertRaises(HTTPException):
            user_profile_handler.register(self.register_data)

    def test_user_login(self):
        """
        Test user login and store JWT in cookie.
        """
        user_profile_handler = UsernamePasswordUserProfile()
        user_profile_handler.register(self.register_data)

        response = user_profile_handler.login(self.login_data, self.ip)
        self.assertIsInstance(response, JSONResponse)
        body = json.loads(response.body.decode("utf-8"))
        self.assertEqual(body["message"], "Login success")

        cookie_header = response.headers.get("set-cookie")
        self.assertIn("access_token", cookie_header)
        self.assertIn("HttpOnly", cookie_header)
        self.assertIn("Max-Age=3600", cookie_header)
        token = cookie_header.split("access_token=")[1].split(";")[0]
        decode_data = user_profile_handler.token_handler.decode(token)
        user_database = UserDatabase()
        retrieved_user = user_database.query(self.register_data["user_name"])
        self.assertEqual(int(decode_data["sub"]), retrieved_user.user_id)
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())

        with self.assertRaises(HTTPException):
            user_profile_handler.login(self.wrong_data, self.ip)


if __name__ == "__main__":
    unittest.main()
