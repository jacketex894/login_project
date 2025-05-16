FROM python:3.13-slim

RUN pip install poetry==2.1.1

WORKDIR /app

RUN apt-get update

COPY ./poetry.lock pyproject.toml /app/

RUN poetry install 

COPY ./ /app/

CMD ["sh", "-c", "poetry run uvicorn main:app --host 0.0.0.0 --port $EXPENSE_SERVICE_PORT --reload"]