from fastapi import APIRouter, Request, HTTPException, Depends

from model.transaction_database import TransactionData
from controller.transaction import create_transaction
from core.error import DatabaseCreateTransactionError, make_error_content, ErrorResponse
from core.token import JWTToken

router = APIRouter()


def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    token_handler = JWTToken()
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    payload = token_handler.decode(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return user_id


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
def create_transaction_record(
    create_transaction_request: TransactionData,
    user: str = Depends(get_current_user_from_cookie),
) -> dict:
    """
    Create a new transaction record.

    Args:
        create_transaction_request (TransactionData) : The transaction data to be inserted.
    """
    create_transaction(user, create_transaction_request)
    return {"message": "Transaction created successfully"}
