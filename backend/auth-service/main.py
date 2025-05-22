from fastapi import FastAPI, Request
from typing import TypedDict
from typing import Union

from util.UserProfile import UsernamePasswordUserProfile, RegisterRequest, LoginRequest

app = FastAPI()


class ErrorResponse(TypedDict):
    detail: str
    code: int


@app.put(
    "/api/register",
    tags=["users"],
    response_model=Union[dict, ErrorResponse],
    responses={
        400: {"model": ErrorResponse, "description": "User name or mail exist error"}
    },
)
def user_register(register_request: RegisterRequest, request: Request):
    """
    Register a new user.

    Args:
        register_request (RegisterRequest) : The user data to be registered.

    Status code:
        200 : User data register successfully.
        400 : User data valid fail.
        500 : Failed to register data (server problem).
    """
    user_profile_handler = UsernamePasswordUserProfile()
    return user_profile_handler.register(register_request)


@app.post(
    "/api/login",
    tags=["users"],
    response_model=Union[dict, ErrorResponse],
    responses={
        400: {"model": ErrorResponse, "description": "User name or password wrong"}
    },
)
def login(login_request: LoginRequest, request: Request):
    """
    Login user with login information.

    Args:
        login_request (LoginRequest) : The user data to be registered.

    Status code:
        200 : User data register successfully.
        400 : User data valid fail.
        500 : Failed to register data (server problem).
    """
    client_ip = request.client.host
    user_profile_handler = UsernamePasswordUserProfile()
    return user_profile_handler.login(login_request, client_ip)
