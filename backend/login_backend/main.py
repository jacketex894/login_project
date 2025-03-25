from fastapi import FastAPI
from typing import TypedDict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.get("/hello-world")
async def hello_world():
    return {"message":"hello"}
    
class LoginRequest(TypedDict):
    account:str
    password:str

@app.post("/api/login")
async def login(loginrequest:LoginRequest):
    return {"message":"login"}