from fastapi import status


class BaseAPIException(Exception):
    error_name: str
    status_code: int
    detail: str
    error_code: int

    def to_dict(self):
        return {
            "error_name": self.error_name,
            "status_code": self.status_code,
            "detail": self.detail,
            "error_code": self.error_code,
        }


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


class DatabaseUpdateUserError(BaseAPIException):
    """Raised when the update user fail."""

    error_name = "DatabaseUpdateUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to update user"
    error_code = 5003


class DatabaseDeleteUserError(BaseAPIException):
    """Raised when the delete user fail."""

    error_name = "DatabaseDeleteUserError"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Failed to delete user"
    error_code = 5004


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


def make_error_content(error_types: list[BaseAPIException]):
    content = {"application/json": {"example": {}}}
    errors_as_dicts = [cls().to_dict() for cls in error_types]
    for error in errors_as_dicts:
        content["application/json"]["example"][error["error_name"]] = {
            "detail": error["detail"],
            "error_code": error["error_code"],
        }
    return content
