from DatabaseFactory import DataBase, DataBaseFactory
from sqlalchemy import Column, Integer, String, TIMESTAMP, create_engine

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
total_amount
date
category
comment
user_name
"""


class ExpenseDatabase(DataBase):
    class Transaction(Base):
        __tablename__ = "transactions"

        transactoion_id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(Integer, nullable=False)
        category = Column(String(100))
        product_name = Column(String(255), nullable=False)
        quantity = Column(Integer, nullable=False, default=1)
        total_amount = Column(Float, nullable=False)
        pay_by = Column(String(255), nullable=False, default="cash")
        date = Column(DateTime, nullable=False)

    def create(self):
        pass

    def query(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
