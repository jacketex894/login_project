from fastapi import FastAPI,Request
from typing import TypedDict
from typing import Union

from .util.UserProfile import UserProfileFactory,RegisterRequest
app = FastAPI()

class ErrorResponse(TypedDict):
    detail: str
    code: int

@app.put("/api/register",tags=["users"], response_model=Union[dict, ErrorResponse], responses={400: {"model": ErrorResponse,
                                                                                   "description":"User name or mail exist error"}})
def user_register(register_request:RegisterRequest, request: Request):
    client_ip = request.client.host 
    return UserProfileFactory.register('Normal',register_request,client_ip)


class LoginRequest(TypedDict):
    account:str
    password:str

@app.post("/api/login",tags=["users"])
async def login(loginrequest:LoginRequest):
    return {"message":"login"}
