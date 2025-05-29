from abc import ABC, abstractmethod
import bcrypt


class Hash(ABC):
    """
    This class define interface for implementing hashing and
    verification method.
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Hashes given password and return resulting hashed string.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The resulting hashed password string.
        """

    @abstractmethod
    def verify(self, password: str, hashed: bytes) -> bool:
        """
        Verify given password with hash_password which store in database.

        Args:
            password (str): The password that needs to be verified.
            hashed (bytes): The hashed password stored in the database.

        Returns:
            bool: True if verification was successful, False otherwise.
        """


class HashBcrypt(Hash):
    """
    Implementation of the Hash interface using bcrypt algorithm
    for password hashing and verification.
    """

    def hash_password(self, password: str) -> str:
        """
        Hash the given plain text password using bcrypt.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The resulting bcrypt hashed password as a UTF-8 string.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        """
        Verify a plain text password against a given bcrypt hashed password.

        Args:
            password (str): The plain text password to verify.
            hashed (str): The bcrypt hashed password to compare against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
