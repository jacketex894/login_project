from fastapi import status
from typing import TypedDict


class BaseAPIException(Exception):
    """
    Base exception class for errors.

    Attributes:
        error_name : str
            A string representing the name/type of the error.
        status_code : int
            The associated HTTP status code (e.g., 400, 404, 500).
        detail : str
            A detailed description of the error, useful for clients.
        error_code : int
            An application-specific error code to help identify
            the exact error type programmatically.
    """

    error_name: str
    status_code: int
    detail: str
    error_code: int

    def to_dict(self) -> dict:
        """
        Convert the exception attributes to a dictionary.
        """
        return {
            "error_name": self.error_name,
            "status_code": self.status_code,
            "detail": self.detail,
            "error_code": self.error_code,
        }


# Server error 5XX
class InvalidHashedPassword(BaseAPIException):
    """Raised when the password does not appear to be properly hashed."""

    error_name = "InvalidHashedPassword"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Invalid hashed password format"
    error_code = 5001


class DatabaseCreateUserError(BaseAPIException):
    """Raised when the create user fail."""

    error_name = "DatabaseCreateUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to create user"
    error_code = 5002


class DatabaseQueryUserError(BaseAPIException):
    """Raised when the query user fail."""

    error_name = "DatabaseQueryUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to query user"
    error_code = 5003


class DatabaseUpdateUserError(BaseAPIException):
    """Raised when the update user fail."""

    error_name = "DatabaseUpdateUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to update user"
    error_code = 5004


class DatabaseDeleteUserError(BaseAPIException):
    """Raised when the delete user fail."""

    error_name = "DatabaseDeleteUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to delete user"
    error_code = 5005


class DatabaseCreateTransactionError(BaseAPIException):
    """Raised when the create transaction error."""

    error_name = "DatabaseCreateTransactionError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to create transaction"
    error_code = 5006


class DatabaseQueryTransactionError(BaseAPIException):
    """Raised when the query transaction error."""

    error_name = "DatabaseQueryTransactionError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to query transaction"
    error_code = 5007


class DatabaseUpdateTransactionError(BaseAPIException):
    """Raised when the update transaction error."""

    error_name = "DatabaseUpdateTransactionError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to update transaction"
    error_code = 5008


class DatabaseDeleteTransactionError(BaseAPIException):
    """Raised when the delete transaction error."""

    error_name = "DatabaseDeleteTransactionError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to delete transaction"
    error_code = 5009


# User error 4XX
class UsernameAlreadyExistsError(BaseAPIException):
    """Raised when the create user name exist."""

    error_name = "UsernameAlreadyExistsError"
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Failed to create user cause of user exist"
    error_code = 4001


class DatabaseQueryUserNotFoundError(BaseAPIException):
    """Raised when the queried user is not found."""

    error_name = "DatabaseQueryUserNotFoundError"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"
    error_code = 4002


class DatabaseUpdateUserNotFoundError(BaseAPIException):
    """Raised when the update user didn't exist."""

    error_name = "DatabaseUpdateUserNotFoundError"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User to update not found"
    error_code = 4003


class DatabaseDeleteUserNotFoundError(BaseAPIException):
    """Raised when the delete user didn't exist."""

    error_name = "DatabaseDeleteUserNotFoundError"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User to delete not found"
    error_code = 4004


class LoginWithWrongPasswordError(BaseAPIException):
    """Raised when the password verify fail."""

    error_name = "LoginWithWrongPasswordError"
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"
    error_code = 4005


class InvalidUserNameOrPassword(BaseAPIException):
    """Raised when authentication fails due to an invalid username or password."""

    error_name = "LoginWithWrongPasswordError"
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"
    error_code = 4006


class DatabaseUpdateTransactionNotFoundError(BaseAPIException):
    """Raised when the update transaction not found."""

    error_name = "DatabaseUpdateTransactionNotFoundError"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Transaction to update not found"
    error_code = 4007


class DatabaseDeleteTransactionNotFoundError(BaseAPIException):
    """Raised when the update transaction not found."""

    error_name = "DatabaseUpdateTransactionNotFoundError"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Transaction to delete not found"
    error_code = 4008


class AccessTokenNotFound(BaseAPIException):
    """Exception raised when the access token is missing from the request."""

    error_name = "AccessTokenNotFound"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Access token not found from the request"
    error_code = 4009


class AccessTokenUserIDNotFound(BaseAPIException):
    """Exception raised when the decoded access token does not contain a user ID."""

    error_name = "AccessTokenUserIDNotFound"
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Access token does not contain a user ID"
    error_code = 4010


class AccessTokenExpired(BaseAPIException):
    """Exception raised when the access token has expired."""

    error_name = "AccessTokenExpired"
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Access token has expired"
    error_code = 4011


class AccessTokenInvalid(BaseAPIException):
    """Exception raised when the access token is invalid or cannot be decoded."""

    error_name = "AccessTokenInvalid"
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Access token is invalid"
    error_code = 4012


class ErrorResponse(TypedDict):
    """error response for api"""

    detail: str
    error_code: int


def make_error_content(error_types: list[BaseAPIException]):
    """
    Output a content for api doc.
    """
    content = {"application/json": {"example": {}}}
    errors_as_dicts = [cls().to_dict() for cls in error_types]
    for error in errors_as_dicts:
        content["application/json"]["example"][error["error_name"]] = {
            "detail": error["detail"],
            "error_code": error["error_code"],
        }
    return content
