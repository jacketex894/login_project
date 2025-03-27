import unittest
import pymysql
from fastapi import HTTPException
import logging

from ..util.UserProfile import UserProfileFactory,RegisterRequest
from ..lib.Database import UserDB

logging.getLogger().addHandler(logging.NullHandler())
class TestUserDB(unittest.TestCase):
    def setUp(self):
        self.request_data:RegisterRequest = {
            "user_name": "test_user",
            "password": "test_password",
            "mail": "test_mail@example.com",
        }
        self.ip = "127.0.0.1"
    def tearDown(self):
        delete_user = UserDB.query_user(self.request_data['user_name'])
        UserDB.delete_user(delete_user)
    def test_user_register(self):
        response = UserProfileFactory.register('Normal',self.request_data,self.ip)
        self.assertEqual(response,{"message": "User successfully registered", "user_name": self.request_data['user_name']})

        #Duplicate Registration
        with self.assertRaises(HTTPException):
            UserProfileFactory.register('Normal',self.request_data,self.ip)

if __name__ == '__main__':
    unittest.main()