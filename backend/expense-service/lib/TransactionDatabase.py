from sqlalchemy import Column, Integer, String, Float, DateTime
from typing import TypedDict,Literal, Optional
from sqlalchemy.ext.declarative import declarative_base
import logging
from fastapi import HTTPException

from .Database import DataBase
"""
item

id
product_name
quantity
user_name
"""

"""
expense

id
product_name
quantity
total_cost
date
category
comment
user_name
"""

class TransactionData(TypedDict):
    """
    A class to represent data which create expense record need

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
    user_id : int
    category : String
    product_name : String
    quantity : int|None
    total_cost : int
    pay_by: String|None
    date:DateTime

class QueryTransactionData(TypedDict):
    """
    A class to represent data which query expense record need

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
    user_id : int|None
    category : str|None
    product_name : str|None
    pay_by: str|None
    date:DateTime|None

class TransactionDatabase(DataBase):
    """
    A class to represent a database of expenses.

    Methods:
    --------
    create(TransactionData):
        creare one transaction  in database.
    
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

    def create(self,transaction_data:TransactionData):
        session = self.session()
        try:
            new_transaction_record = self.Transaction(
                user_id = transaction_data["user_id"],
                category = transaction_data["category"],
                product_name = transaction_data["product_name"],
                quantity = transaction_data["quantity"],
                total_cost = transaction_data["total_cost"],
                pay_by = transaction_data["pay_by"],
                date = transaction_data["date"]
            )
            session.add(new_transaction_record)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error("Error occurred when create transaction record: %s", e)
            raise HTTPException(
                status_code=500,
            ) from e
        finally:
            session.close()
    def query(self,query_data:TransactionData):
        session = self.session()
        query = session.query(self.Transaction)
        if query_data['user_id'] is not None:
            query = query.filter(self.Transaction.user_id == query_data['user_id'])
    
        if query_data['category'] is not None:
            query = query.filter(self.Transaction.category == query_data['category'] )
        
        if query_data['product_name'] is not None:
            query = query.filter(self.Transaction.product_name == query_data['product_name'])
        
        if query_data['pay_by'] is not None:
            query = query.filter(self.Transaction.pay_by == query_data['pay_by'])
        
        if query_data['date'] is not None:
            query = query.filter(self.Transaction.date == query_data['date'])
        session.close()
        return query.all()

    def update(self):
        pass

    def delete(self):
        pass
