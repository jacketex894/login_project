from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine
from sqlalchemy.orm import sessionmaker
from typing import TypedDict
import logging
from fastapi import HTTPException

from config.config import Config
from .DatabaseFactory import DataBaseFactory, DataBase


class UserData(TypedDict):
    user_name: str
    hashed_password: str
    mail: str
    created_at: TIMESTAMP
    last_login_ip: str


class UserDatabaseFactory(DataBaseFactory):
    """
    The factory use to create connection to mysql database.
    Interacting with table members
    """

    _instance = None
    database_instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UserDatabaseFactory, cls).__new__(cls)
        return cls._instance

    def get_database(self) -> DataBase:
        if self.database_instance is None:
            self.database_instance = UserDatabase(Config.USER_DATABASE_URL)
        return self.database_instance


class UserDatabase(DataBase):
    class User(declarative_base()):
        __tablename__ = "members"

        user_id = Column(Integer, primary_key=True, autoincrement=True)
        user_name = Column(String(255), unique=True, nullable=False)
        hashed_password = Column(String(255), nullable=False)
        mail = Column(String(255), unique=True, nullable=False)
        created_at = Column(TIMESTAMP)
        last_login_ip = Column(String(45))

    def __init__(self, db_url: str):
        engine = create_engine(db_url)
        self.Session = sessionmaker(bind=engine)

    def check_hash_password(self, hashed_password: str) -> bool:
        if len(hashed_password) < 60:
            logging.error(f"hashed_password {hashed_password} is not hashed.")
            raise HTTPException(
                status_code=500,
            )

    def create(self, user_data: UserData) -> None:
        self.check_hash_password(user_data["hashed_password"])
        session = self.Session()
        try:
            new_user = self.User(
                user_name=user_data["user_name"],
                hashed_password=user_data["hashed_password"],
                mail=user_data["mail"],
                created_at=user_data["created_at"],
                last_login_ip=user_data["last_login_ip"],
            )
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error occurred: {e}")
            raise HTTPException(
                status_code=400,
            )
        finally:
            session.close()

    def query(self, user_name: str) -> User | None:
        session = self.Session()
        query_user = (
            session.query(self.User).filter(self.User.user_name == user_name).first()
        )
        session.close()
        return query_user.all()

    def update(self, user_name: str, hashed_paaword: str, mail: str) -> None:
        # shouldn't store any password without hash
        self.check_hash_password(hashed_paaword)
        session = self.Session()
        try:
            update_user = (
                session.query(self.User)
                .filter(self.User.user_name == user_name)
                .first()
            )
            if update_user:
                update_user.hashed_password = hashed_paaword
                update_user.mail = mail
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error occurred: {e}")
        finally:
            session.close()

    def delete(self, user: User) -> None:
        session = self.Session()
        try:
            session.delete(user)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error occurred: {e}")
        finally:
            session.close()
