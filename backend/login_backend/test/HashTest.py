import unittest
from argon2.exceptions import VerifyMismatchError

from ..lib.Hash import HashFactory

class TestBcrypt(unittest.TestCase):
    def setUp(self):
        self.password = "test_password"
        self.hash_method = HashFactory.get_hash_method('bcrypt')
    
    def test_hash_password(self):
        hashed_password = self.hash_method.hash_password(self.password)

        self.assertIsInstance(hashed_password, str)
        self.assertTrue(len(hashed_password) > 0)

        # The same password but different hash should be unique
        hashed_password_2 = self.hash_method.hash_password(self.password)
        self.assertNotEqual(hashed_password, hashed_password_2)
    
    def test_verify_password_valid(self):
        hashed_password = self.hash_method.hash_password(self.password)
        self.assertTrue(self.hash_method.verify(self.password, hashed_password))
        self.assertFalse(self.hash_method.verify("wrong_password", hashed_password))

class TestArgon2(unittest.TestCase):
    def setUp(self):
        self.password = "test_password"
        self.hash_method = HashFactory.get_hash_method('argon2')
    
    def test_hash_password(self):
        hashed_password = self.hash_method.hash_password(self.password)

        self.assertIsInstance(hashed_password, str)
        self.assertTrue(len(hashed_password) > 0)

        # The same password but different hash should be unique
        hashed_password_2 = self.hash_method.hash_password(self.password)
        self.assertNotEqual(hashed_password, hashed_password_2)
    
    def test_verify_password_valid(self):
        hashed_password = self.hash_method.hash_password(self.password)
        self.assertTrue(self.hash_method.verify(self.password, hashed_password))
        with self.assertRaises(VerifyMismatchError):
            self.hash_method.verify("wrong_password", hashed_password)

if __name__ == '__main__':
    unittest.main()