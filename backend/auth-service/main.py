from fastapi import FastAPI,Request
from typing import TypedDict
from typing import Union

from util.UserProfile import UserProfileFactory,RegisterRequest,LoginRequest
app = FastAPI()

class ErrorResponse(TypedDict):
    detail: str
    code: int

@app.put("/api/register",tags=["users"], response_model=Union[dict, ErrorResponse], responses={400: {"model": ErrorResponse,
                                                                                   "description":"User name or mail exist error"}})
def user_register(register_request:RegisterRequest, request: Request):
    client_ip = request.client.host 
    user_profile_handler = UserProfileFactory.get_profile_handler('UsernamePassword')
    return user_profile_handler.register(register_request,client_ip)



@app.post("/api/login",tags=["users"], response_model=Union[dict, ErrorResponse], responses={400: {"model": ErrorResponse,
                                                                                   "description":"User name or password wrong"}})
async def login(login_request:LoginRequest, request: Request):
    client_ip = request.client.host
    user_profile_handler = UserProfileFactory.get_profile_handler('UsernamePassword')
    return user_profile_handler.login(login_request,client_ip)
