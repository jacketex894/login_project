import unittest
from datetime import datetime
import logging
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError

from model.user_database import UserDatabase, UserData
from model.hash import HashBcrypt
from core.error import (
    InvalidHashedPassword,
    DatabaseCreateUserError,
    UsernameAlreadyExistsError,
    DatabaseQueryUserError,
    DatabaseQueryUserNotFoundError,
    DatabaseUpdateUserNotFoundError,
    DatabaseUpdateUserError,
    DatabaseDeleteUserNotFoundError,
    DatabaseDeleteUserError,
)

logging.getLogger().addHandler(logging.NullHandler())


class TestUserDB(unittest.TestCase):
    """
    Test case for interacting with the user database.
    """

    def setUp(self):
        self.request_data: UserData = {
            "user_name": "test_user",
            "hashed_password": "test_password",
            "mail": "test_mail@example.com",
            "created_at": datetime(2025, 5, 29, 3, 36, 24, 776730),
        }
        self.hash_method = HashBcrypt()
        self.user_data: UserData = {
            "user_name": "test_user",
            "hashed_password": self.hash_method.hash_password("test_password"),
            "mail": "test_mail@example.com",
            "created_at": datetime(2025, 5, 29, 3, 36, 24, 776730),
        }
        self.user_database = UserDatabase()

    def test_create_user_success(self):
        """Test that a valid user is created successfully in the database."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        with patch(
            "model.user_database.UserDatabase.User", return_value=mock_user
        ), patch.object(self.user_database, "session", return_value=mock_session):
            self.user_database.create(self.user_data)
            self.user_database.User.assert_called_once_with(
                user_name=self.user_data["user_name"],
                hashed_password=self.user_data["hashed_password"],
                mail=self.user_data["mail"],
                created_at=self.user_data["created_at"],
            )
            mock_session.add.assert_called_once_with(mock_user)
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_create_user_failure(self):
        """Test that a valid user is created fail in the database."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        with patch(
            "model.user_database.UserDatabase.User", return_value=mock_user
        ), patch.object(self.user_database, "session", return_value=mock_session):
            mock_session.commit.side_effect = SQLAlchemyError("DB Error")

            with self.assertRaises(DatabaseCreateUserError):
                self.user_database.create(self.user_data)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_create_user_duplicate(self):
        """Test that a valid user is already created in the database."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        integrity_error = IntegrityError(
            statement="INSERT INTO users ...",
            params={},
            orig=Exception("Duplicate entry 'test_user' for key 'users.user_name'"),
        )

        with patch(
            "model.user_database.UserDatabase.User", return_value=mock_user
        ), patch.object(self.user_database, "session", return_value=mock_session):
            mock_session.commit.side_effect = integrity_error

            with self.assertRaises(UsernameAlreadyExistsError):
                self.user_database.create(self.user_data)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_query_user_success(self):
        """Test that querying a user by user_name returns the correct user."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_user

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            result = self.user_database.query("test_user")

            self.assertEqual(result, mock_user)

            mock_session.query.assert_called_once_with(self.user_database.User)
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()
            mock_session.close.assert_called_once()

    def test_query_user_not_found(self):
        """Test that querying a user not in the database raises exception."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseQueryUserNotFoundError):
                self.user_database.query("nonexistent_user")

            mock_session.query.assert_called_once_with(self.user_database.User)
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()
            mock_session.close.assert_called_once()

    def test_query_user_user_fail(self):
        """Test that querying a user fail."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.side_effect = SQLAlchemyError("DB Error")

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseQueryUserError):
                self.user_database.query("test_user")

            mock_session.query.assert_called_once_with(self.user_database.User)
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()
            mock_session.close.assert_called_once()

    def test_update_user_success(self):
        """Test that updating an existing user succeeds."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_user

        update_hash_password = self.hash_method.hash_password("hashed_password_example")

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            self.user_database.update(
                user_id=1, hashed_paaword=update_hash_password, mail="test@example.com"
            )

            mock_session.query.assert_called_once_with(self.user_database.User)
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()

            self.assertEqual(mock_user.hashed_password, update_hash_password)
            self.assertEqual(mock_user.mail, "test@example.com")

            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_update_user_not_exist(self):
        """Test that updating a non-existent user raises error."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        update_hash_password = self.hash_method.hash_password("hashed_password_example")

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseUpdateUserNotFoundError):
                self.user_database.update(
                    user_id=999,
                    hashed_paaword=update_hash_password,
                    mail="test@example.com",
                )

            mock_session.close.assert_called_once()

    def test_update_user_failure(self):
        """Test that a SQLAlchemyError during commit raises DatabaseUpdateUserError."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_user

        mock_session.commit.side_effect = SQLAlchemyError("DB Error")

        update_hash_password = self.hash_method.hash_password("hashed_password_example")

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseUpdateUserError):
                self.user_database.update(
                    user_id=1,
                    hashed_paaword=update_hash_password,
                    mail="test@example.com",
                )

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    def test_delete_user_success(self):
        """Test that deleting an existing user succeeds."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_user

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            self.user_database.delete(user_id=1)

            mock_session.query.assert_called_once_with(self.user_database.User)
            mock_query.filter.assert_called_once()
            mock_filter.first.assert_called_once()

            mock_session.delete.assert_called_once_with(mock_user)
            mock_session.commit.assert_called_once()
            mock_session.close.assert_called_once()

    def test_delete_user_not_exist(self):
        """Test that deleting a non-existent user raises DatabaseDeleteUserNotFoundError."""
        mock_session = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = None

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseDeleteUserNotFoundError):
                self.user_database.delete(user_id=999)

            mock_session.close.assert_called_once()

    def test_delete_user_failure(self):
        """Test that SQLAlchemyError during commit raises DatabaseDeleteUserError."""
        mock_session = MagicMock()
        mock_user = MagicMock()

        mock_query = mock_session.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_filter.first.return_value = mock_user

        mock_session.commit.side_effect = SQLAlchemyError("DB Error")

        with patch(
            "model.user_database.UserDatabase.User", new_callable=MagicMock
        ), patch.object(self.user_database, "session", return_value=mock_session):
            with self.assertRaises(DatabaseDeleteUserError):
                self.user_database.delete(user_id=1)

            mock_session.rollback.assert_called_once()
            mock_session.close.assert_called_once()

    # TODO:need to study Integration Testing
    def test_crud(self):
        """
        Test the basic CRUD operations (Create, Read, Update, Delete) on the user database.
        """
        # insert
        # validates only trigger in real orm model
        with self.assertRaises(InvalidHashedPassword):
            self.user_database.create(self.request_data)
        self.user_database.create(self.user_data)

        # query
        retrieved_user = self.user_database.query(self.user_data["user_name"])
        self.assertIsNotNone(retrieved_user, "retrieved_user should not be None")
        self.assertEqual(retrieved_user.user_name, self.user_data["user_name"])

        # update
        update_mail = "update_mail@example.com"
        update_password = "update_password"
        hashed_paaword = self.hash_method.hash_password(update_password)
        self.user_database.update(retrieved_user.user_id, hashed_paaword, update_mail)
        updated_user = self.user_database.query(self.user_data["user_name"])
        self.assertEqual(updated_user.mail, update_mail)
        self.assertEqual(updated_user.hashed_password, hashed_paaword)

        # delete
        self.user_database.delete(retrieved_user.user_id)
        with self.assertRaises(DatabaseDeleteUserNotFoundError):
            self.user_database.delete(self.user_data["user_name"])


if __name__ == "__main__":
    unittest.main()
