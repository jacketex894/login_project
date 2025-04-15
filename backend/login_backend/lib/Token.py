from abc import ABC,abstractmethod
import jwt
from datetime import datetime,timedelta

from ..config import Config
class TokenStrategy(ABC):
    @abstractmethod
    def encode(self,data:dict) -> str:
        pass
    @abstractmethod
    def decode(self,token:str) -> dict:
        pass

class JWTToken(TokenStrategy):
    def encode(self, data):
        encode_data = data.copy()
        encode_data.update({'exp':datetime.now()+timedelta(minutes=Config.JWT_EXPIRE_MINUTES)})
        return  jwt.encode(encode_data, Config.JWT_SECRET_KEY, algorithm=Config.JWT_ALGORITHM)
    def decode(self, token):
        return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])

class Token:
    def __init__(self, token_method:TokenStrategy):
        self.TokenHandler = token_method
    def encode(self,data):
        return self.TokenHandler.encode(data)
    def decode(self,token):
        return self.TokenHandler.decode(token)
    