from fastapi import FastAPI

from lib.TransactionDatabase import TransactionData
from util.Transaction import create_transaction

app = FastAPI()


@app.post("/expense/transaction")
def create_transaction_record(create_transaction_request: TransactionData) -> dict:
    """
    Create a new transaction record.

    Args:
        create_transaction_request (TransactionData) : The transaction data to be inserted.

    Status code:
        200 : Transaction record create successfully.
        500 : Failed to create transaction record.
    """
    create_transaction(create_transaction_request)
    return {"message": "Transaction created successfully"}
