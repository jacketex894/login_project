import unittest
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock

from model.transaction_database import (
    TransactionData,
    QueryTransactionData,
    TransactionDatabase,
)
from controller.transaction import create_transaction, query_user_transactions


class TestTransaction(unittest.TestCase):
    """
    Test case for transaction-related function.
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

    def test_create_transaction(self):
        """
        Test the creation of a new transaction.
        """
        create_transaction(0, self.transaction_data)
        transction_database = TransactionDatabase()
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
        transction_database.delete(retrieved_data[0].transaction_id)

        # TODO: update item db relate function

    @patch("controller.transaction.TransactionDatabase")
    def test_get_user_transactions(self, mock_database_class):
        """
        Test retrieving transactions for a specific user
        """
        mock_instance = MagicMock()
        mock_transaction1 = MagicMock()
        mock_transaction1.to_dict.return_value = {
            "transaction_id": 0,
            "user_id": 0,
            "category": "food",
            "product_name": "apple",
            "quantity": 1,
            "total_cost": 10,
            "pay_by": "cash",
            "date": datetime(2025, 1, 1),
        }
        mock_transaction2 = MagicMock()
        mock_transaction2.to_dict.return_value = {
            "transaction_id": 1,
            "user_id": 0,
            "category": "food",
            "product_name": "banana",
            "quantity": 1,
            "total_cost": 20,
            "pay_by": "cash",
            "date": datetime(2025, 1, 1),
        }
        mock_instance.query.return_value = [mock_transaction1, mock_transaction2]
        mock_database_class.return_value = mock_instance
        excepted_data = [
            {
                "transaction_id": 0,
                "category": "food",
                "product_name": "apple",
                "quantity": 1,
                "total_cost": 10,
                "pay_by": "cash",
                "date": datetime(2025, 1, 1),
            },
            {
                "transaction_id": 1,
                "category": "food",
                "product_name": "banana",
                "quantity": 1,
                "total_cost": 20,
                "pay_by": "cash",
                "date": datetime(2025, 1, 1),
            },
        ]

        data = query_user_transactions({"user_id": 0})
        self.assertEqual(data, excepted_data)


if __name__ == "__main__":
    unittest.main()
