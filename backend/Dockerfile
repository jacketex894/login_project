FROM python:3.13-slim

RUN pip install poetry==2.1.1

WORKDIR /app

RUN apt-get update

COPY poetry.lock pyproject.toml ./

COPY login_backend ./login_backend

RUN poetry install && rm -rf $POETRY_CACHE_DIR

#set PATH for poetry
ENV PATH="/root/.local/bin:${PATH}"

CMD ["sh", "-c", "poetry run uvicorn login_backend.main:app --host 0.0.0.0 --port $BACKEND_PORT --reload"]
