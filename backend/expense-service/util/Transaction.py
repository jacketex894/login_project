from lib.TransactionDatabase import TransactionData, TransactionDatabase


def create_transaction(transaction_data: TransactionData) -> None:
    """
    Create a new transaction record.

    Args:
        transaction_data (TransactionData) : The transaction data to be inserted.

    Status code:
        200 : Transaction record create successfully.
        500 : Failed to create transaction record.
    """
    transaction_database = TransactionDatabase()
    transaction_database.create(transaction_data)

    # TODO: update item db with transaction data
