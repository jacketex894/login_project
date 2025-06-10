from abc import ABC, abstractmethod
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from fastapi import Request

from core.config.config import Config
from core.error import (
    AccessTokenNotFound,
    AccessTokenUserIDNotFound,
    AccessTokenExpired,
    AccessTokenInvalid,
)


class TokenStrategy(ABC):
    """Abstract base class for implementing token encoding and decoding strategies."""

    @abstractmethod
    def encode(self, data: dict) -> str:
        """Encodes a dictionary of data into a token string.

        Args:
            data (dict): The data to encode into the token.

        Returns:
            str: The encoded token as a string.
        """

    @abstractmethod
    def decode(self, token: str) -> dict:
        """Decodes a token string back into a dictionary of data.

        Args:
            token (str): The token to decode.

        Returns:
            dict: The decoded data as a dictionary.
        """


class JWTToken(TokenStrategy):
    """JWT-based implementation of the TokenStrategy interface."""

    def encode(self, data):
        """
        Encodes a dictionary into a JWT token with an expiration time.
        Args:
            data (dict): The data to include in the token payload.
        Returns:
            str: A JWT-encoded string.
        """
        encode_data = data.copy()
        encode_data.update(
            {"exp": datetime.now() + timedelta(minutes=Config.JWT_EXPIRE_MINUTES)}
        )
        return jwt.encode(
            encode_data, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM
        )

    def decode(self, token):
        """
        Decodes a JWT token into its original dictionary form.
        Args:
            token (str): The JWT token string to decode.

        Returns:
            dict: The decoded token payload.
        """
        try:
            decode_data = jwt.decode(
                token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM]
            )
        except ExpiredSignatureError as e:
            raise AccessTokenExpired from e
        except InvalidTokenError as e:
            raise AccessTokenInvalid from e
        return decode_data


class TokenService:
    """A service class that handles token generation and extraction using a strategy pattern."""

    def __init__(self, strategy: TokenStrategy):
        """
        Initializes the TokenService with a specific token strategy.

        Args:
           strategy (TokenStrategy): The token strategy implementation to use (e.g., JWTToken).
        """

        self.token_handler = strategy()

    def generate_token(self, data: dict) -> str:
        """
        Generates a token from the given user data.

        Args:
            data (dict): The data to encode into the token.

        Returns:
            str: The encoded token string.
        """
        return self.token_handler.encode(data)

    def get_current_user_from_cookie(self, request: Request) -> int:
        """
        Extracts and decodes the token from the request's cookie to retrieve user information.

        Args:
            request (Request): The HTTP request containing the cookie.

        Returns:
            dict: The decoded user information from the token.
        """
        token = request.cookies.get("access_token")
        if token is None:
            raise AccessTokenNotFound
        payload = self.token_handler.decode(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise AccessTokenUserIDNotFound
        return int(user_id)
