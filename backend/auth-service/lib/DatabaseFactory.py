from abc import ABC, abstractmethod
from typing import Any


class DataBase(ABC):
    """
    This class define interface for interacting with a
    database system.
    """

    @abstractmethod
    def create(self):
        """Create new data."""
        pass

    @abstractmethod
    def query(self) -> Any:
        """query data."""
        pass

    @abstractmethod
    def update(self):
        """update data."""
        pass

    @abstractmethod
    def delete(self):
        """delete data."""
        pass


class DataBaseFactory(ABC):
    """
    The factory is used to create database connections.
    Each table corresponds to its own factory.
    The factory should also follow the singleton pattern to avoid creating additional connections.
    """

    @abstractmethod
    def get_database(self) -> DataBase:
        """Create or get a singleton product"""
        pass
