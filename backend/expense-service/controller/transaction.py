from typing import Dict

from model.transaction_database import TransactionData, TransactionDatabase


# TODO: add user to transaction_data
def create_transaction(user, transaction_data: TransactionData) -> None:
    """
    Create a new transaction record.

    Args:
        transaction_data (TransactionData) : The transaction data to be inserted.
    """
    transaction_database = TransactionDatabase()
    transaction_data["user_id"] = user
    transaction_database.create(transaction_data)

    # TODO: update item db with transaction data


def query_user_transactions(user_id: int) -> Dict:
    """
    Retrieve a dict of transactions for a specific user.

    Args:
        user_id (int) : The unique identifier of the user.
    Returns:
        dict: A dictionary of transaction records.
        Each transaction uses the transaction ID as the key and the transaction data as the value.
    """
    transaction_database = TransactionDatabase()
    data = transaction_database.query({"user_id": user_id})
    transactions = [transaction.to_dict() for transaction in data]
    for transaction in transactions:
        del transaction["user_id"]
    return transactions
