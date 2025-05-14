from abc import ABC, abstractmethod
from typing import Any

class DataBase():
    @abstractmethod
    def create():
        pass
    @abstractmethod
    def query() -> Any:
        pass
    @abstractmethod
    def update():
        pass
    @abstractmethod
    def delete():
        pass

class DataBaseFactory(ABC):
    @abstractmethod
    def get_database(self) -> DataBase:
        pass