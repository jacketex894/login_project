import unittest
from argon2.exceptions import VerifyMismatchError

from model.hash import HashBcrypt


class TestBcrypt(unittest.TestCase):
    """
    Test case for hash with the user bctypt.
    """

    def setUp(self):
        self.password = "test_password"
        self.hash_method = HashBcrypt()

    def test_hash_password(self):
        """
        Test hash password
        """
        hashed_password = self.hash_method.hash_password(self.password)

        self.assertIsInstance(hashed_password, str)
        self.assertTrue(len(hashed_password) > 0)

        # The same password but different hash should be unique
        hashed_password_2 = self.hash_method.hash_password(self.password)
        self.assertNotEqual(hashed_password, hashed_password_2)

    def test_verify_password_valid(self):
        """
        Test verify password
        """
        hashed_password = self.hash_method.hash_password(self.password)
        self.assertTrue(self.hash_method.verify(self.password, hashed_password))
        self.assertFalse(self.hash_method.verify("wrong_password", hashed_password))


if __name__ == "__main__":
    unittest.main()
