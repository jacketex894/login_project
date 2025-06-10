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
