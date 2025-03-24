from abc import ABC, abstractmethod

class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self,pasword:str) -> str:
        pass
    @abstractmethod
    def verify(self,password:str,hashed:str)-> bool:
        pass