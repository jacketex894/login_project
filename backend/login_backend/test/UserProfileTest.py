import unittest
from fastapi import HTTPException
import logging
from datetime import datetime

from ..util.UserProfile import UserProfileFactory,RegisterRequest,LoginRequest
from ..lib.Database import UserDB

logging.getLogger().addHandler(logging.NullHandler())
class TestUserDB(unittest.TestCase):
    def setUp(self):
        self.register_data:RegisterRequest = {
            "user_name": "test_user",
            "password": "test_password",
            "mail": "test_mail@example.com",
        }
        self.login_data:LoginRequest = {
            "user_name": "test_user",
            "password": "test_password",
        }
        self.ip = "127.0.0.1"
    def tearDown(self):
        delete_user = UserDB.query_user(self.register_data['user_name'])
        UserDB.delete_user(delete_user)

    def test_user_register(self):
        user_profile_handler = UserProfileFactory.get_profile_handler('UsernamePassword')
        response = user_profile_handler.register(self.register_data,self.ip)
        self.assertEqual(response,{"message": "User successfully registered", "user_name": self.register_data['user_name']})

        #Duplicate Registration
        with self.assertRaises(HTTPException):
            user_profile_handler.register(self.register_data,self.ip)

    
    def test_user_login(self):
        user_profile_handler = UserProfileFactory.get_profile_handler('UsernamePassword')
        user_profile_handler.register(self.register_data,self.ip)
        
        response = user_profile_handler.login(self.login_data,self.ip)
        decode_data = user_profile_handler.token_handler.decode(response)
        self.assertEqual(decode_data['user_name'],self.login_data['user_name'])
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())


if __name__ == '__main__':
    unittest.main()