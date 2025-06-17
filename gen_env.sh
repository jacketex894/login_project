#!/bin/bash
ENV_FILE="./.env"
ENV_SAMPLE_FILE="env_template"

if [ ! -f "$ENV_FILE" ]; then
  echo ".env file does not exist, generating a new one from envsample..."
  ENV_SAMPLE_CONTENT=$(cat "$ENV_SAMPLE_FILE")

  AUTH_SERVICE_PORT=$((RANDOM % 10001 + 10000))
  EXPENSE_SERVICE_PORT=$((RANDOM % 10001 + 10000))
  DATABASE_PORT=$((RANDOM % 10001 + 10000))
  MYSQL_ROOT_PASSWORD=$(openssl rand -base64 12 | tr -dc 'A-Za-z0-9' | head -c 16)
  TOKEN_SECRET_KEY=$(openssl rand -base64 12 | tr -dc 'A-Za-z0-9' | head -c 16)
  NEW_ENV_CONTENT=$(echo "$ENV_SAMPLE_CONTENT" | \
        sed "s/AUTH_SERVICE_PORT=[^ ]*/AUTH_SERVICE_PORT=$AUTH_SERVICE_PORT/" | \
        sed "s/EXPENSE_SERVICE_PORT=[^ ]*/EXPENSE_SERVICE_PORT=$EXPENSE_SERVICE_PORT/" | \
        sed "s/DATABASE_PORT=[^ ]*/DATABASE_PORT=$DATABASE_PORT/" | \
        sed "s/MYSQL_ROOT_PASSWORD=[^ ]*/MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD/" | \
        sed "s/TOKEN_SECRET_KEY=[^ ]*/TOKEN_SECRET_KEY=$TOKEN_SECRET_KEY/")
  echo "$NEW_ENV_CONTENT" > "$ENV_FILE"
fi