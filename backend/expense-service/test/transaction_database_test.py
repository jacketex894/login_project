import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
import logging
from unittest.mock import call

from model.transaction_database import (
    TransactionDatabase,
    TransactionData,
    QueryTransactionData,
)
from core.error import (
    DatabaseCreateTransactionError,
    DatabaseQueryTransactionError,
    DatabaseUpdateTransactionNotFoundError,
    DatabaseUpdateTransactionError,
    DatabaseDeleteTransactionNotFoundError,
    DatabaseDeleteTransactionError,
)

logging.getLogger().addHandler(logging.NullHandler())


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
        self.transaction_database = TransactionDatabase()

    def test_create_transaction_sucess(self):
        """Test create a transaction successful."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        with patch(
            "model.transaction_database.TransactionDatabase.Transaction",
            return_value=mock_transaction,
        ), patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            self.transaction_database.create(self.transaction_data)
            self.transaction_database.Transaction.assert_called_once_with(
                user_id=self.transaction_data["user_id"],
                category=self.transaction_data["category"],
                product_name=self.transaction_data["product_name"],
                quantity=self.transaction_data["quantity"],
                total_cost=self.transaction_data["total_cost"],
                pay_by=self.transaction_data["pay_by"],
                date=self.transaction_data["date"],
            )
            mock_session.add.assert_called_once_with(mock_transaction)
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_create_transaction_fail(self):
        """Test create a transaction fail."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        with patch(
            "model.transaction_database.TransactionDatabase.Transaction",
            return_value=mock_transaction,
        ), patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            mock_session.commit.side_effect = SQLAlchemyError("DB Error")

            with self.assertRaises(DatabaseCreateTransactionError):
                self.transaction_database.create(self.transaction_data)

                mock_session.rollback.assert_called_once()
                mock_session.close.assert_called_once()

    def test_query_transaction_success(self):
        """Test query a transaction successful."""
        mock_session = MagicMock()
        mock_transaction_1 = MagicMock()
        mock_transaction_2 = MagicMock()
        mock_transactions = [mock_transaction_1, mock_transaction_2]

        mock_query = mock_session.query.return_value
        mock_query.filter.side_effect = lambda *args, **kwargs: mock_query
        mock_query.all.return_value = mock_transactions
        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            results = self.transaction_database.query(self.query_data)

            self.assertEqual(results, mock_transactions)
            mock_session.query.assert_called_once_with(
                self.transaction_database.Transaction
            )
            self.assertEqual(mock_query.filter.call_count, 4)
            mock_query.all.assert_called_once()
            mock_session.close.assert_called_once()

    def test_query_transaction_fail(self):
        """Test query a transaction fail."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_query.filter.return_value = mock_query
        mock_query.all.side_effect = SQLAlchemyError("DB Error")

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            with self.assertRaises(DatabaseQueryTransactionError):
                self.transaction_database.query(self.query_data)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_update_transaction_success(self):
        """Test update a transaction successfully."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_transaction

        with patch(
            "model.transaction_database.TransactionDatabase.Transaction",
            return_value=mock_transaction,
        ), patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            self.transaction_database.update(1, self.transaction_data)

            mock_session.query.assert_called_once_with(
                self.transaction_database.Transaction
            )
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()

            self.assertEqual(mock_transaction.user_id, self.transaction_data["user_id"])
            self.assertEqual(
                mock_transaction.category, self.transaction_data["category"]
            )
            self.assertEqual(
                mock_transaction.product_name, self.transaction_data["product_name"]
            )
            self.assertEqual(
                mock_transaction.quantity, self.transaction_data["quantity"]
            )
            self.assertEqual(
                mock_transaction.total_cost, self.transaction_data["total_cost"]
            )
            self.assertEqual(mock_transaction.pay_by, self.transaction_data["pay_by"])
            self.assertEqual(mock_transaction.date, self.transaction_data["date"])

            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_update_transaction_not_found(self):
        """Test update when no transaction record is found."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            with self.assertRaises(DatabaseUpdateTransactionNotFoundError):
                self.transaction_database.update(1, self.transaction_data)

            mock_session.close.assert_called_once()

    def test_update_transaction_db_error(self):
        """Test update raises SQLAlchemyError and rolls back."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_transaction

        mock_session.commit.side_effect = SQLAlchemyError("DB Error")

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            with self.assertRaises(DatabaseUpdateTransactionError):
                self.transaction_database.update(1, self.transaction_data)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_delete_transaction_success(self):
        """Test deleting a transaction successfully."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_transaction

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            self.transaction_database.delete(1)

            mock_session.query.assert_called_once_with(
                self.transaction_database.Transaction
            )
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()
            mock_session.delete.assert_called_once_with(mock_transaction)
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_delete_transaction_not_found(self):
        """Test deleting a transaction that does not exist."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            with self.assertRaises(DatabaseDeleteTransactionNotFoundError):
                self.transaction_database.delete(1)

            mock_session.delete.assert_not_called()
            mock_session.commit.assert_not_called()
            mock_session.rollback.assert_not_called()
            mock_session.close.assert_called_once()

    def test_delete_transaction_db_error(self):
        """Test deleting a transaction when a SQLAlchemyError occurs."""
        mock_session = MagicMock()
        mock_transaction = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_transaction

        mock_session.commit.side_effect = SQLAlchemyError("DB Error")

        with patch.object(
            self.transaction_database, "session", return_value=mock_session
        ):
            with self.assertRaises(DatabaseDeleteTransactionError):
                self.transaction_database.delete(1)

            mock_session.delete.assert_called_once_with(mock_transaction)
            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_crud(self):
        """
        Test the basic CRUD operations (Create, Read, Update, Delete) on the transaction database.
        """
        # transction_database = TransactionDatabase()
        # create
        self.transaction_database.create(self.transaction_data)

        # query
        retrieved_data = self.transaction_database.query(self.query_data)
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
        self.transaction_database.update(retrieved_data[0].transaction_id, update_data)
        retrieved_data = self.transaction_database.query(self.query_data)
        self.assertEqual(retrieved_data[0].product_name, update_data["product_name"])

        # delete
        self.transaction_database.delete(retrieved_data[0].transaction_id)
        with self.assertRaises(DatabaseDeleteTransactionNotFoundError):
            self.transaction_database.delete(retrieved_data[0].transaction_id)


if __name__ == "__main__":
    unittest.main()
