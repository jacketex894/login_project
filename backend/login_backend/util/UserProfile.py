from abc import ABC,abstractmethod
from typing import TypedDict
from datetime import datetime
import logging

from ..lib.Hash import HashFactory
from ..lib.Database import UserDB,UserData

class RegisterRequest(TypedDict):
    user_name:str
    password:str
    mail:str

class User_profile(ABC):
    @abstractmethod
    def register():
        pass
    @abstractmethod
    def login():
        pass

class NormalUserProfile(User_profile):
    def register(self,register_request:RegisterRequest,client_ip:str) -> dict:
        hash_password = HashFactory.get_hash_method("bcrypt").hash_password(register_request['password'])
        new_user = UserData(
            user_name = register_request['user_name'],
            hashed_password = hash_password,
            mail = register_request['mail'],
            created_at = datetime.now(),
            last_login_ip = client_ip
        )
        UserDB.insert_user(new_user)
        return {"message": "User successfully registered", "user_name": register_request['user_name']}
    def login():
        pass
class UserProfileFactory():
    @staticmethod
    def register(register_type:str,register_request:RegisterRequest,client_ip:str) -> dict:
        if register_type == 'Normal':
            User_profile_handler = NormalUserProfile()
        else:
            logging.error(f"user progild method {register_type} is not exist.")
        return User_profile_handler.register(register_request,client_ip)
