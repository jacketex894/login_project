import unittest
from fastapi import HTTPException
import logging
from datetime import datetime
from fastapi.responses import JSONResponse
import json

from util.UserProfile import UserProfileFactory, RegisterRequest, LoginRequest
from lib.UserDatabase import UserDatabaseFactory

logging.getLogger().addHandler(logging.NullHandler())


class TestUserProfile(unittest.TestCase):
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
        database_factory = UserDatabaseFactory()
        user_database = database_factory.get_database()
        delete_user = user_database.query(self.register_data["user_name"])
        user_database.delete(delete_user)

    def test_user_register(self):
        user_profile_handler = UserProfileFactory.get_profile_handler(
            "UsernamePassword"
        )
        response = user_profile_handler.register(self.register_data, self.ip)
        self.assertIsInstance(response, JSONResponse)

        body = json.loads(response.body.decode("utf-8"))
        self.assertEqual(body["message"], "User successfully registered")
        self.assertEqual(body["user_name"], self.register_data["user_name"])
        # Duplicate Registration
        with self.assertRaises(HTTPException):
            user_profile_handler.register(self.register_data, self.ip)

    def test_user_login(self):
        user_profile_handler = UserProfileFactory.get_profile_handler(
            "UsernamePassword"
        )
        user_profile_handler.register(self.register_data, self.ip)

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
        self.assertEqual(decode_data["user_name"], self.login_data["user_name"])
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())

        with self.assertRaises(HTTPException):
            user_profile_handler.login(self.wrong_data, self.ip)


if __name__ == "__main__":
    unittest.main()
