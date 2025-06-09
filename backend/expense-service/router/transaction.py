from fastapi import APIRouter

from model.transaction_database import TransactionData
from controller.transaction import create_transaction
from core.error import DatabaseCreateTransactionError, make_error_content, ErrorResponse

router = APIRouter()


@router.post(
    "/expense/transaction",
    tags=["expense"],
    response_model=dict,
    responses={
        500: {
            "model": ErrorResponse,
            "content": make_error_content([DatabaseCreateTransactionError]),
        },
    },
)
def create_transaction_record(create_transaction_request: TransactionData) -> dict:
    """
    Create a new transaction record.

    Args:
        create_transaction_request (TransactionData) : The transaction data to be inserted.
    """
    create_transaction(create_transaction_request)
    return {"message": "Transaction created successfully"}
