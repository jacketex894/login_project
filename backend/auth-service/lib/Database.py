from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import TypedDict
import logging
from fastapi import HTTPException

from config.config import Config

engine = create_engine(Config.USER_DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'members'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), unique=True,nullable=False)
    hashed_password = Column(String(255), nullable=False)
    mail = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP)
    last_login_ip = Column(String(45))

class UserData(TypedDict):
    user_name:str
    hashed_password:str
    mail:str
    created_at:TIMESTAMP
    last_login_ip:str


def check_hash_password(hashed_password: str) -> bool:
    if len(hashed_password) < 60:
        logging.error(f"hashed_password {hashed_password} is not hashed.")
        raise HTTPException(
            status_code=500,
        )
    
class UserDB:
    @staticmethod
    def insert_user(user_data:UserData) -> None:

        #shouldn't store any password without hash
        check_hash_password(user_data['hashed_password'])
        session = Session()
        try:
            new_user = User(user_name = user_data['user_name'],
                            hashed_password = user_data['hashed_password'],
                            mail = user_data['mail'],
                            created_at = user_data['created_at'],
                            last_login_ip = user_data['last_login_ip'])
            session.add(new_user)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f'Error occurred: {e}')
            raise HTTPException(
                status_code=400,
            )
        finally:
            session.close()

    @staticmethod
    def query_user(user_name:str) -> User|None:
        session = Session()
        query_user = session.query(User).filter(User.user_name == user_name).first()
        session.close()
        return query_user
    
    @staticmethod
    def update_user(user_name:str,hashed_paaword:str,mail:str) -> None:
        #shouldn't store any password without hash
        check_hash_password(hashed_paaword)
        session = Session()
        try:
            update_user = session.query(User).filter(User.user_name == user_name).first()
            if update_user:
                update_user.hashed_password = hashed_paaword
                update_user.mail = mail
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f'Error occurred: {e}')
        finally:
            session.close()

    @staticmethod
    def delete_user(user:User) -> None:
        session = Session()
        try:
            session.delete(user)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f'Error occurred: {e}')
        finally:
            session.close()
