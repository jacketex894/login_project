from fastapi import FastAPI
from typing import TypedDict
from fastapi.middleware.cors import CORSMiddleware

from system.lib.hash import hash_password

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/hello-world")
async def hello_world():
    return {"message":"hello"}
    
class LoginRequest(TypedDict):
    account:str
    password:str

@app.post("/login")
async def login(loginrequest:LoginRequest):
    print(loginrequest)
    print(f"Hashed Password: {hash_password(loginrequest['password'])}")
    return {"message":"login"}