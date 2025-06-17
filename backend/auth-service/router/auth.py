from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from core.error import (
    BaseAPIException,
    make_error_content,
    InvalidHashedPassword,
    DatabaseCreateUserError,
    UsernameAlreadyExistsError,
    InvalidUserNameOrPassword,
    ErrorResponse,
)
from controller.user_profile import (
    UsernamePasswordUserProfile,
    RegisterRequest,
    LoginRequest,
)

router = APIRouter()


@router.post(
    "/register",
    tags=["users"],
    response_model=dict,
    responses={
        500: {
            "model": ErrorResponse,
            "content": make_error_content(
                [InvalidHashedPassword, DatabaseCreateUserError]
            ),
        },
        400: {
            "model": ErrorResponse,
            "content": make_error_content([UsernameAlreadyExistsError]),
        },
    },
)
def user_register(register_request: RegisterRequest, request: Request):
    """
    Register a new user.

    Args:
        register_request (RegisterRequest) : The user data to be registered.
    """
    user_profile_handler = UsernamePasswordUserProfile()
    try:
        result = user_profile_handler.register(register_request)
        return JSONResponse(content=result, status_code=200)
    except BaseAPIException as e:
        error = e.to_dict()
        raise HTTPException(
            status_code=error["status_code"], detail=error["detail"]
        ) from e


@router.post(
    "/login",
    tags=["users"],
    response_model=dict,
    responses={
        400: {
            "model": ErrorResponse,
            "content": make_error_content([InvalidUserNameOrPassword]),
        },
    },
)
def login(login_request: LoginRequest, request: Request):
    """
    Login user with login information.

    Args:
        login_request (LoginRequest) : The user data to be registered.
    """
    try:
        client_ip = request.client.host
        user_profile_handler = UsernamePasswordUserProfile()
        result, token = user_profile_handler.login(login_request, client_ip)
        response = JSONResponse(content=result, status_code=200)
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
    except BaseAPIException as e:
        error = InvalidUserNameOrPassword().to_dict()
        raise HTTPException(
            status_code=error["status_code"], detail=error["detail"]
        ) from e
