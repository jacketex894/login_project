from abc import ABC, abstractmethod
from typing import TypedDict
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from lib.Hash import HashFactory
from lib.UserDatabase import UserDatabase, UserData
from lib.Token import JWTToken


class RegisterRequest(TypedDict):
    """
    Represents a request payload for user registration.

    Attributes:
        user_name (str): The desired username of the new user.
        password (str): The user's password in plain text.
        mail (str): The user's email address.
    """

    user_name: str
    password: str
    mail: str


class LoginRequest(TypedDict):
    """
    Represents a request payload for user login.

    Attributes:
        user_name (str): The username of the user attempting to log in.
        password (str): The corresponding password for the user account.
    """

    user_name: str
    password: str


class UserProfile(ABC):
    """
    This class defin the interface for user-related actions such as registration and login.
    """

    @abstractmethod
    def register(self, *args):
        """
        Register a new user with the provided credentials.
        """
        pass

    @abstractmethod
    def login(self, *args):
        """
        Authenticate a user with the given credentials.
        """
        pass


class UsernamePasswordUserProfile(UserProfile):
    """
    This class uses a username and password
    for user registration and authentication.
    """

    def __init__(self):
        self.hash_handler = HashFactory.get_hash_method("bcrypt")
        self.token_handler = JWTToken()
        self.user_database = UserDatabase()

    def register(self, register_request: RegisterRequest) -> dict:
        """
        This function provide register with user name,password and mail.

        Args:
            register_request(RegisterRequest): The user information for register.

        Returns:
            dict: success message and user name
        """
        hash_password = self.hash_handler.hash_password(register_request["password"])
        new_user = UserData(
            user_name=register_request["user_name"],
            hashed_password=hash_password,
            mail=register_request["mail"],
            created_at=datetime.now(),
        )
        self.user_database.create(new_user)
        return JSONResponse(
            content={
                "message": "User successfully registered",
                "user_name": register_request["user_name"],
            }
        )

    # TODO: add login log and email check
    # TODO: add table to record login history
    def login(self, login_request: LoginRequest, client_ip: str) -> str | bool:
        """
        This function provide login with user name and password.
        After succes login , probide jwt in cookie.

        Args:
            login_request(LoginRequest): The user information for login.

        Returns:
            dict: success message
        """
        retrieved_user = self.user_database.query(login_request["user_name"])
        valid = self.hash_handler.verify(
            login_request["password"], retrieved_user.hashed_password
        )
        if valid:
            encode_data = {"sub": str(retrieved_user.user_id)}
            token = self.token_handler.encode(encode_data)
            response = JSONResponse(content={"message": "Login success"})
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                max_age=3600,
                expires=3600,
                samesite="Strict",
                secure=True,
            )
            return response
        else:
            raise HTTPException(
                status_code=400,
            )
