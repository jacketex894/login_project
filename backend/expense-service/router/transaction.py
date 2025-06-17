from fastapi import APIRouter, Request, HTTPException, Depends

from model.transaction_database import TransactionData
from controller.transaction import create_transaction
from core.error import (
    DatabaseCreateTransactionError,
    DatabaseQueryTransactionError,
    make_error_content,
    ErrorResponse,
)
from core.token import JWTToken, TokenService
from controller.transaction import query_user_transactions

router = APIRouter()


@router.post(
    "/transaction",
    tags=["expense"],
    response_model=dict,
    responses={
        500: {
            "model": ErrorResponse,
            "content": make_error_content([DatabaseCreateTransactionError]),
        },
    },
)
def create_transaction_record(
    create_transaction_request: TransactionData,
    user: str = Depends(TokenService(JWTToken).get_current_user_from_cookie),
) -> dict:
    """
    Create a new transaction record.

    Args:
        create_transaction_request (TransactionData) : The transaction data to be inserted.
    """
    create_transaction(user, create_transaction_request)
    return {"message": "Transaction created successfully"}


@router.get(
    "/transaction",
    tags=["expense"],
    response_model=dict,
    responses={
        500: {
            "model": ErrorResponse,
            "content": make_error_content([DatabaseQueryTransactionError]),
        },
    },
)
def query_user_transaction_records(
    user_id: int = Depends(TokenService(JWTToken).get_current_user_from_cookie),
) -> dict:
    """
    Query transaction records for a specific user.

    Returns: A dictionary of transaction records.
    """
    return {"transactions": query_user_transactions(user_id)}
