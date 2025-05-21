from typing import TypedDict
import logging
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from config.config import Config
from .Database import DataBase


class UserData(TypedDict):
    """
    A class to represent data which create user data need

    user_name : str
        The unique username of the user.
    hashed_password : str
        The hashed password for the user.
    mail : str
        The unique email address of the user.
    created_at : datetime
        The timestamp when the user account is created.
    """

    user_name: str
    hashed_password: str
    mail: str
    created_at: datetime


class UserDatabase(DataBase):
    """
    A class to manage CRUD (Create, Read, Update, Delete) operations for user data.

    Methods:
        check_hash_password(self) -> bool:
            Check password is hash or not.
        create(user_data:dict) -> None:
            Create a new user with provided data.
        query(user_name:str) -> dict:
            Retrivew a user's information by user name.
        update(user_name: str, hashed_password: str, mail: str) -> bool:
            Update a exist user information by user_name using hashed_password and mail.
        delete(user_id:int) -> bool:
            Delete the user data by user_id
    """

    class User(declarative_base()):
        """
        A class to represent table "users" data structure

        user_id : int
            The unique identifier for the transaction (Primary Key).
        user_name : str
            The user's unique username. Cannot be null.
        hashed_password : str
            The user's hashed password. Cannot be null.
        mail : str
            The user's unique email address. Cannot be null.
        created_at : datetime
            The datetime indicating when the user was created.
        """

        __tablename__ = "users"

        user_id = Column(Integer, primary_key=True, autoincrement=True)
        user_name = Column(String(255), unique=True, nullable=False)
        hashed_password = Column(String(255), nullable=False)
        mail = Column(String(255), unique=True, nullable=False)
        created_at = Column(DateTime, nullable=False)

    def check_hash_password(self, hashed_password: str) -> bool:
        """
        Ensure the password is hashed before saving.

        Args:
            hashed_password (str) : The user's password. Must be verified as hashed before storing in the database.

        Returns:
            bool: True if verify was successful, False otherwise.
        """
        if len(hashed_password) < 60:
            logging.error("hashed_password %s is not hashed.", hashed_password)
            raise HTTPException(
                status_code=500,
            )

    def create(self, user_data: UserData) -> None:
        """
        Insert a user data into the database.

        Args:
            user_data (UserData) : The user data to be inserted.
        """
        self.check_hash_password(user_data["hashed_password"])
        session = self.session()
        try:
            new_user = self.User(
                user_name=user_data["user_name"],
                hashed_password=user_data["hashed_password"],
                mail=user_data["mail"],
                created_at=user_data["created_at"],
            )
            session.add(new_user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logging.error("Error occurred while creating user data: %s", e)
            raise HTTPException(
                status_code=500, detail="Creating user data error"
            ) from e
        finally:
            session.close()

    def query(self, user_name: str) -> User:
        """
        Query user data from the database that match the given user name.

        Args:
            user_name (str) : The user name used to filter user data.

        Returns:
            list[Transaction]: A list of transaction records that match the conditions specified in `query_data`.
        """
        session = self.session()
        retrieved_user = (
            session.query(self.User).filter(self.User.user_name == user_name).first()
        )
        session.close()
        return retrieved_user

    def update(self, user_id: int, hashed_paaword: str, mail: str):
        """
        Update the user data in the database that matches the given user_id.

        Args:
            user_id (int) : The ID used to filter user data.
            hashed_paaword (str) : The hashed password used to update user data.
            mail(str) : The mail used to update user data.
        """
        self.check_hash_password(hashed_paaword)
        session = self.session()
        try:
            update_user = (
                session.query(self.User).filter(self.User.user_id == user_id).first()
            )
            if update_user:
                update_user.hashed_password = hashed_paaword
                update_user.mail = mail
                session.commit()
            else:
                logging.error(
                    "Error occurred while update user data: User doesn't exist"
                )
                raise HTTPException(status_code=500, detail="User doesn't exist")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error("Error occurred while update user data: %s", e)
            raise HTTPException(status_code=500, detail="Update user data error") from e
        finally:
            session.close()

    def delete(self, user_id: int) -> None:
        """
        Delete the user data in the database that matches the given user_id.

        Args:
            user_id (int) : The ID used to filter user data.
        """
        session = self.session()
        try:
            user = session.query(self.User).filter(self.User.user_id == user_id).first()
            if user:
                session.delete(user)
                session.commit()
            else:
                logging.error(
                    "Error occurred while delete user data: User doesn't exist"
                )
                raise HTTPException(status_code=500, detail="User doesn't exist")
        except SQLAlchemyError as e:
            session.rollback()
            logging.error(
                "Error occurred while deleting user data for user id %d: %s",
                user_id,
                e,
            )
            raise HTTPException(
                status_code=500,
            ) from e
        finally:
            session.close()
