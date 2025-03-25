from abc import ABC, abstractmethod
import bcrypt
from argon2 import PasswordHasher

class Hash(ABC):
    @abstractmethod
    def hash_password(self,pasword:str) -> str:
        pass
    @abstractmethod
    def verify(self,password:str,hashed:bytes)-> bool:
        pass

class hash_bcrypt(Hash):
    @staticmethod
    def hash_password(password) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    @staticmethod
    def verify(password:str,hash_password:str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

class hash_argon2(Hash):
    @staticmethod
    def hash_password(password) -> str:
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        return hashed_password
    @staticmethod
    def verify(password:str,hash_password:str) -> bool:
        ph = PasswordHasher()
        return ph.verify(hash_password,password)
    
class HashFactory():
    @staticmethod
    def get_hash_method(hash_type:str) -> Hash:
        match hash_type:
            case 'bcrypt':
                return hash_bcrypt()
            case 'argon2':
                return hash_argon2()

