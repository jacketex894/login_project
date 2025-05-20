FROM python:3.13-slim

RUN pip install poetry==2.1.1

WORKDIR /app

RUN apt-get update

COPY ./poetry.lock pyproject.toml /app/

RUN poetry install 

#set PATH for poetry
ENV PATH="/root/.local/bin:${PATH}"

COPY ./ /app/

CMD ["sh", "-c", "poetry run uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT --reload"]