import unittest
from datetime import datetime
from unittest.mock import patch, Mock
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Request

from core.token import JWTToken, TokenService
from core.error import (
    AccessTokenNotFound,
    AccessTokenUserIDNotFound,
    AccessTokenExpired,
    AccessTokenInvalid,
)


class TestToken(unittest.TestCase):
    """
    Test case for token.
    """

    def setUp(self):
        self.token_handler = JWTToken()
        self.data = {
            "user_id": "0",
        }

    def test_generate_token(self):
        """
        Test generate jwt token.
        """
        token = self.token_handler.encode(self.data)
        decode_data = self.token_handler.decode(token)
        self.assertEqual(decode_data["user_id"], self.data["user_id"])
        self.assertIn("exp", decode_data)
        self.assertGreater(decode_data["exp"], datetime.now().timestamp())

    @patch("core.token.jwt.decode")
    def test_decode_raises_access_token_expired(self, mock_jwt_decode):
        """
        Test that decode raises AccessTokenExpired when jwt.decode raises ExpiredSignatureError.
        """
        mock_jwt_decode.side_effect = ExpiredSignatureError()

        with self.assertRaises(AccessTokenExpired):
            self.token_handler.decode("expired.jwt.token")

    @patch("core.token.jwt.decode")
    def test_decode_raises_access_token_invalid(self, mock_jwt_decode):
        """
        Test that decode raises AccessTokenInvalid when jwt.decode raises InvalidTokenError.
        """
        mock_jwt_decode.side_effect = InvalidTokenError()

        with self.assertRaises(AccessTokenInvalid):
            self.token_handler.decode("invalid.jwt.token")


class TestTokenServiceMethods(unittest.TestCase):
    def setUp(self):
        """Create a mock token_handler and TokenService for testing."""
        self.mock_strategy = Mock()
        self.token_service = TokenService(lambda: self.mock_strategy)
        self.mock_request = Mock(spec=Request)
        self.mock_request.cookies = Mock()

    def test_generate_token_success(self):
        """Test generate_token returns the result of token_handler.encode()."""
        self.mock_strategy.encode.return_value = "mocked_token"
        data = {"user": "test"}

        result = self.token_service.generate_token(data)

        self.mock_strategy.encode.assert_called_once_with(data)
        self.assertEqual(result, "mocked_token")

    def test_miss_token_cookie(self):
        """Test get_current_user_from_cookie raises AccessTokenNotFound if no token cookie."""
        self.mock_request.cookies.get.return_value = None

        with self.assertRaises(AccessTokenNotFound):
            self.token_service.get_current_user_from_cookie(self.mock_request)

    def test_token_not_contain_sub(self):
        """Test get_current_user_from_cookie raises AccessTokenUserIDNotFound if 'sub' is not in payload."""
        self.mock_request.cookies.get.return_value = "example"
        self.mock_strategy.decode.return_value = {"not_sub": 1}

        with self.assertRaises(AccessTokenUserIDNotFound):
            self.token_service.get_current_user_from_cookie(self.mock_request)

    def test_get_current_user_success(self):
        """Test get_current_user_from_cookie returns user ID if token is valid and contains 'sub'."""
        self.mock_request.cookies.get.return_value = "example"
        self.mock_strategy.decode.return_value = {"sub": 42}

        user_id = self.token_service.get_current_user_from_cookie(self.mock_request)

        self.assertEqual(user_id, 42)


if __name__ == "__main__":
    unittest.main()
