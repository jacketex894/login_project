from fastapi import status


class InvalidHashedPassword(Exception):
    """Raised when the password does not appear to be properly hashed."""


class DatabaseCreateUserError(Exception):
    """Raised when the create user fail."""


class UsernameAlreadyExistsError(Exception):
    """Raised when the create user name exist."""


class DatabaseQueryUserNotFoundError(Exception):
    """Raised when the queried user is not found."""


class DatabaseUpdateUserNotFoundError(Exception):
    """Raised when the update user didn't exist."""


class DatabaseUpdateUserError(Exception):
    """Raised when the update user fail."""


class DatabaseDeleteUserNotFoundError(Exception):
    """Raised when the delete user didn't exist."""


class DatabaseDeleteUserError(Exception):
    """Raised when the delete user fail."""


class LoginWithWrongPasswordError(Exception):
    """Raised when the password verify fail."""


HANDLED_ERRORS = {
    InvalidHashedPassword: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Invalid hashed password format",
    ),
    DatabaseCreateUserError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Failed to create user",
    ),
    UsernameAlreadyExistsError: (
        status.HTTP_400_BAD_REQUEST,
        "Failed to create user",
    ),
    DatabaseQueryUserNotFoundError: (status.HTTP_404_NOT_FOUND, "User not found"),
    DatabaseUpdateUserNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "User to update not found",
    ),
    DatabaseUpdateUserError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Failed to update user",
    ),
    DatabaseDeleteUserNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "User to delete not found",
    ),
    DatabaseDeleteUserError: (
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Failed to delete user",
    ),
    LoginWithWrongPasswordError: (
        status.HTTP_401_UNAUTHORIZED,
        "Invalid username or password",
    ),
}
