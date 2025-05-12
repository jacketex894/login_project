from abc import ABC,abstractmethod
from typing import TypedDict
from datetime import datetime
import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from lib.Hash import HashFactory
from lib.Database import UserDB,UserData
from lib.Token import Token,JWTToken

class RegisterRequest(TypedDict):
    user_name:str
    password:str
    mail:str

class LoginRequest(TypedDict):
    user_name:str
    password:str

class User_profile(ABC):
    @abstractmethod
    def register():
        pass
    @abstractmethod
    def login():
        pass

class UsernamePasswordUserProfile(User_profile):
    def __init__(self):
        self.hash_handler = HashFactory.get_hash_method("bcrypt")
        self.token_handler = Token(JWTToken())

    def register(self,register_request:RegisterRequest,client_ip:str) -> dict:
        hash_password = self.hash_handler.hash_password(register_request['password'])
        new_user = UserData(
            user_name = register_request['user_name'],
            hashed_password = hash_password,
            mail = register_request['mail'],
            created_at = datetime.now(),
            last_login_ip = client_ip
        )
        UserDB.insert_user(new_user)
        return JSONResponse(content = {"message": "User successfully registered", "user_name": register_request['user_name']})
    
    #TODO: add login log and email check
    def login(self,login_request:LoginRequest,client_ip:str) -> str|bool:
        retrieved_user = UserDB.query_user(login_request['user_name'])
        valid = self.hash_handler.verify(login_request['password'],retrieved_user.hashed_password)
        if valid:
            encode_data = {
                'user_name':login_request['user_name']
            }
            token = self.token_handler.encode(encode_data)
            response = JSONResponse(content={"message": "Login success"})
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,         
                max_age=3600,         
                expires=3600,
                samesite="Lax",        
                secure=True           
            )
            return  response 
        else:
            raise HTTPException(
                status_code=400,
            )
        


class UserProfileFactory():
    @staticmethod
    def get_profile_handler(type:str) -> User_profile:
        if type == 'UsernamePassword':
            return UsernamePasswordUserProfile()
        else:
            logging.error(f"user progild method {type} is not exist.")

