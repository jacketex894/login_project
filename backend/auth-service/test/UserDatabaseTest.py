import unittest
from datetime import datetime
from fastapi import HTTPException
import logging

from lib.UserDatabase import UserDatabaseFactory,UserData
from lib.Hash import HashFactory

logging.getLogger().addHandler(logging.NullHandler())
class TestUserDB(unittest.TestCase):
    def setUp(self):
        self.request_data:UserData = {
            "user_name": "test_user",
            "hashed_password": "test_password",
            "mail": "test_mail@example.com",
            "created_at": datetime.now(),  
            "last_login_ip": "127.0.0.1"
        }
        self.hash_method = HashFactory.get_hash_method('bcrypt')
        self.user_data:UserData = {
            "user_name": "test_user",
            "hashed_password": self.hash_method.hash_password("test_password"),
            "mail": "test_mail@example.com",
            "created_at": datetime.now(),  
            "last_login_ip": "127.0.0.1"
        }
    def test_CRUD(self):
        database_factory = UserDatabaseFactory()
        user_database = database_factory.get_database()

        #insert
        with self.assertRaises(HTTPException):
            user_database.create(self.request_data)
        user_database.create(self.user_data)
        
        #query
        retrieved_user = user_database.query(self.user_data["user_name"])
        self.assertIsNotNone(retrieved_user, "retrieved_user should not be None")
        self.assertEqual(retrieved_user.user_name, self.user_data["user_name"])

        #update
        update_mail = "update_mail@example.com"
        update_password = "update_password"
        hashed_paaword = self.hash_method.hash_password(update_password)
        with self.assertRaises(HTTPException):
             user_database.update(self.user_data["user_name"],update_password,update_mail)
        user_database.update(self.user_data["user_name"],hashed_paaword,update_mail)
        updated_user = user_database.query(self.user_data["user_name"])
        self.assertEqual(updated_user.mail, update_mail)
        self.assertEqual(updated_user.hashed_password, hashed_paaword)

        #delete
        retrieved_user = user_database.query(self.user_data["user_name"])
        user_database.delete(retrieved_user)
        deleted_user = user_database.query(self.user_data["user_name"])
        self.assertIsNone(deleted_user, "deleted_user should be None")

if __name__ == '__main__':
    unittest.main()