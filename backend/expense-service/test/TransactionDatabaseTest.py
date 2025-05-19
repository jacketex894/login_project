import unittest
from datetime import datetime

from lib.TransactionDatabase import TransactionDatabase,TransactionData,QueryTransactionData

class TestTransactionDatabase(unittest.TestCase):
    def setUp(self):
        self.transaction_data: TransactionData = {
            "user_id":0,
            "category":"food",
            "product_name":"pizza",
            "quantity":1,
            "total_cost":200,
            "pay_by":"cash",
            "date":datetime(year=2025,month=1,day=1)
        }
        self.query_data: QueryTransactionData = {
            "user_id":0,
            "category":None,
            "product_name":"pizza",
            "pay_by":None,
            "date":None,
        }

    def test_CRUD(self):
        transction_database = TransactionDatabase()
        # create
        transction_database.create(self.transaction_data)
        # update
        retrieved_data = transction_database.query(self.query_data)
        print(retrieved_data)
        # query
        # delete


if __name__ == "__main__":
    unittest.main()
