from sqlalchemy import Column, Integer, String, Float, DateTime
from typing import TypedDict
from sqlalchemy.ext.declarative import declarative_base
import logging
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List

from core.database import DataBase
from core.error import (
    DatabaseCreateTransactionError,
    DatabaseQueryTransactionError,
    DatabaseUpdateTransactionNotFoundError,
    DatabaseUpdateTransactionError,
    DatabaseDeleteTransactionNotFoundError,
    DatabaseDeleteTransactionError,
)

# TODO: add new database item
"""
item

id
product_name
quantity
user_name
"""


class TransactionData(TypedDict):
    """
    A class to represent data which create transaction record need

    user_id : int
        The ID of the user associated with the transaction.

    category : str
        The category of the transaction (e.g., traffic, entertainment).

    product_name : str
        The name of the product involved in the transaction.

    quantity : int
        The number of items involved in the transaction.

    total_cost : float
        The total amount for the transaction.

    pay_by : str
        The method of payment (e.g., cash, credit card).

    date : datetime
        The date and time when the transaction occurred.
    """

    user_id: int
    category: str
    product_name: str
    quantity: int
    total_cost: int
    pay_by: str
    date: datetime


class QueryTransactionData(TypedDict):
    """
    A class to represent data which query transaction record need

    user_id : int|None
        The ID of the user associated with the transaction.

    category : str|None
        The category of the transaction (e.g., traffic, entertainment).

    product_name : str|None
        The name of the product involved in the transaction.

    pay_by : str|None
        The method of payment (e.g., cash, credit card).

    date : datetime|None
        The date and time when the transaction occurred.
    """

    user_id: int | None
    category: str | None
    product_name: str | None
    pay_by: str | None
    date: DateTime | None


class TransactionDatabase(DataBase):
    """
    A class to represent a database of transaction.

    Methods:
    --------
    create(transaction_data):
        Create a transaction record from transaction_data in the database.
    query(query_data):
        Query transaction records that match all conditions provided in query_data.
    update(transaction_id , update_data)
        Update a transaction record identified by transaction_id using update_data.
    delete(transaction_id)
        Delete the transaction record identified by transaction_id.
    """

    class Transaction(declarative_base()):
        """
        A class to represent table "transactions" data structure

        transaction_id : int
            The unique identifier for the transaction (Primary Key).

        user_id : int
            The ID of the user associated with the transaction (Foreign Key).

        category : str
            The category of the transaction (e.g., traffic, entertainment).

        product_name : str
            The name of the product involved in the transaction.

        quantity : int
            The number of items involved in the transaction.
            If the value is None, it will default to 1.

        total_cost : float
            The total amount for the transaction.

        pay_by : str
            The method of payment (e.g., cash, credit card). Defaults to "cash".
            If the value is None, it will default to “cash”.

        date : datetime
            The date and time when the transaction occurred.
        """

        __tablename__ = "transactions"

        transaction_id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer, nullable=False)
        category = Column(String(100))
        product_name = Column(String(255), nullable=False)
        quantity = Column(Integer, nullable=False, default=1)
        total_cost = Column(Float, nullable=False)
        pay_by = Column(String(255), nullable=False, default="cash")
        date = Column(DateTime, nullable=False)

        def to_dict(self):
            return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def create(self, transaction_data: TransactionData):
        """
        Insert a transaction record into the database.

        Args:
            transaction_data (TransactionData) : The transaction data to be inserted.
        """
        session = self.session()
        try:
            new_transaction_record = self.Transaction(
                user_id=transaction_data["user_id"],
                category=transaction_data["category"],
                product_name=transaction_data["product_name"],
                quantity=transaction_data["quantity"],
                total_cost=transaction_data["total_cost"],
                pay_by=transaction_data["pay_by"],
                date=transaction_data["date"],
            )
            session.add(new_transaction_record)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logging.error("Error occurred while creating transaction record: %s", e)
            raise DatabaseCreateTransactionError from e
        finally:
            session.close()

    def query(self, query_data: TransactionData) -> List[Transaction]:
        """
        Query transaction records from the database that match the given conditions.

        Args:
            query_data (TransactionData) : The data used to filter transaction records.

        Returns:
            list[Transaction]: A list of transaction records that match the conditions specified in `query_data`.
        """
        session = self.session()
        try:
            query = session.query(self.Transaction)
            if query_data.get("user_id") is not None:
                query = query.filter(self.Transaction.user_id == query_data["user_id"])

            if query_data.get("category") is not None:
                query = query.filter(
                    self.Transaction.category == query_data["category"]
                )

            if query_data.get("product_name") is not None:
                query = query.filter(
                    self.Transaction.product_name == query_data["product_name"]
                )

            if query_data.get("pay_by") is not None:
                query = query.filter(self.Transaction.pay_by == query_data["pay_by"])

            if query_data.get("date") is not None:
                query = query.filter(self.Transaction.date == query_data["date"])
            return query.all()
        except SQLAlchemyError as e:
            session.rollback()
            logging.error("Error occurred while query transaction record: %s", e)
            raise DatabaseQueryTransactionError from e
        finally:
            session.close()

    def update(self, transaction_id: int, update_data: TransactionData) -> bool:
        """
        Update the transaction record in the database that matches the given transaction_id.

        Args:
            transaction_id (int) : The ID used to filter transaction records.
            update_data (TransactionData): The data used to update transaction record.
        """

        session = self.session()
        query = session.query(self.Transaction)
        try:
            update_record = query.filter(
                self.Transaction.transaction_id == transaction_id
            ).first()
            if update_record:
                update_record.user_id = update_data["user_id"]
                update_record.category = update_data["category"]
                update_record.product_name = update_data["product_name"]
                update_record.quantity = update_data["quantity"]
                update_record.total_cost = update_data["total_cost"]
                update_record.pay_by = update_data["pay_by"]
                update_record.date = update_data["date"]
            else:
                raise DatabaseUpdateTransactionNotFoundError
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logging.error("Error occurred while updating transaction record: %s", e)
            raise DatabaseUpdateTransactionError from e
        finally:
            session.close()

    def delete(self, transaction_id: int) -> bool:
        """
        Delete the transaction record in the database that matches the given transaction_id.

        Args:
            transaction_id (int) : The ID used to filter transaction records.
        """
        session = self.session()
        try:
            transaction = (
                session.query(self.Transaction)
                .filter(self.Transaction.transaction_id == transaction_id)
                .first()
            )
            if transaction:
                session.delete(transaction)
                session.commit()
            else:
                raise DatabaseDeleteTransactionNotFoundError

        except SQLAlchemyError as e:
            session.rollback()
            logging.error(
                "Error occurred while deleting transaction record for transaction_id %d: %s",
                transaction_id,
                e,
            )
            raise DatabaseDeleteTransactionError from e
        finally:
            session.close()
