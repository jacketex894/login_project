import unittest
from datetime import datetime

from lib.TransactionDatabase import (
    TransactionDatabase,
    TransactionData,
    QueryTransactionData,
)


class TestTransactionDatabase(unittest.TestCase):
    """
    Test case for interacting with the transaction database.
    """

    def setUp(self):
        self.transaction_data: TransactionData = {
            "user_id": 0,
            "category": "food",
            "product_name": "pizza",
            "quantity": 1,
            "total_cost": 200,
            "pay_by": "cash",
            "date": datetime(year=2025, month=1, day=1),
        }
        self.query_data: QueryTransactionData = {
            "user_id": 0,
            "category": "food",
            "product_name": None,
            "pay_by": "cash",
            "date": datetime(year=2025, month=1, day=1),
        }

    def test_crud(self):
        """
        Test the basic CRUD operations (Create, Read, Update, Delete) on the transaction database.
        """
        transction_database = TransactionDatabase()
        # create
        transction_database.create(self.transaction_data)

        # query
        retrieved_data = transction_database.query(self.query_data)
        self.assertIsNotNone(retrieved_data, "retrieved data should not be None")
        self.assertEqual(retrieved_data[0].user_id, self.transaction_data["user_id"])
        self.assertEqual(retrieved_data[0].category, self.transaction_data["category"])
        self.assertEqual(
            retrieved_data[0].product_name, self.transaction_data["product_name"]
        )
        self.assertEqual(retrieved_data[0].quantity, self.transaction_data["quantity"])
        self.assertEqual(
            retrieved_data[0].total_cost, self.transaction_data["total_cost"]
        )
        self.assertEqual(retrieved_data[0].pay_by, self.transaction_data["pay_by"])
        self.assertEqual(retrieved_data[0].date, self.transaction_data["date"])

        # update
        update_data: TransactionData = {
            "user_id": 0,
            "category": "food",
            "product_name": "hamburger",
            "quantity": 1,
            "total_cost": 200,
            "pay_by": "cash",
            "date": datetime(year=2025, month=1, day=1),
        }
        transction_database.update(retrieved_data[0].transaction_id, update_data)
        retrieved_data = transction_database.query(self.query_data)
        self.assertEqual(retrieved_data[0].product_name, update_data["product_name"])

        # delete
        flag = transction_database.delete(retrieved_data[0].transaction_id)
        self.assertTrue(flag)
        flag = transction_database.delete(retrieved_data[0].transaction_id)
        self.assertFalse(flag)


if __name__ == "__main__":
    unittest.main()
