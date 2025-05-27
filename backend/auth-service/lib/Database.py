from abc import ABC, abstractmethod
from typing import Any
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from core.config.config import Config


class DataBase(ABC):
    """
    This class define interface for interacting with a
    database system.
    """

    _instance = None

    def __new__(cls):
        """
        Each database instance should be implemented as a singleton to prevent excessive connection usage.
        """
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        engine = create_engine(Config.USER_DATABASE_URL)
        self.session = sessionmaker(bind=engine)

    @abstractmethod
    def create(self, *args, **kwargs):
        """Create new data."""

    @abstractmethod
    def query(self, *args, **kwargs) -> Any:
        """Query data."""

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update data."""

    @abstractmethod
    def delete(self, *args, **kwargs):
        """Delete data."""
