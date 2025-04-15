#!/bin/bash
ENV_FILE="./.env"
ENV_SAMPLE_FILE="env_template"

if [ ! -f "$ENV_FILE" ]; then
  echo ".env file does not exist, generating a new one from envsample..."
  ENV_SAMPLE_CONTENT=$(cat "$ENV_SAMPLE_FILE")

  BACKEND_PORT=$((RANDOM % 10001 + 10000))
  FRONTEND_PORT=$((RANDOM % 10001 + 10000))
  HTTPS_PORT=$((RANDOM % 10001 + 10000))
  DATABASE_PORT=$((RANDOM % 10001 + 10000))
  MYSQL_ROOT_PASSWORD=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)
  TOKEN_SECRET_KEY=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)
  NEW_ENV_CONTENT=$(echo "$ENV_SAMPLE_CONTENT" | \
        sed "s/BACKEND_PORT=[^ ]*/BACKEND_PORT=$BACKEND_PORT/" | \
        sed "s/FRONTEND_PORT=[^ ]*/FRONTEND_PORT=$FRONTEND_PORT/" | \
        sed "s/HTTPS_PORT=[^ ]*/HTTPS_PORT=$HTTPS_PORT/" | \
        sed "s/DATABASE_PORT=[^ ]*/DATABASE_PORT=$DATABASE_PORT/" | \
        sed "s/MYSQL_ROOT_PASSWORD=[^ ]*/MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD/")
        sed "s/TOKEN_SECRET_KEY=[^ ]*/TOKEN_SECRET_KEY=$TOKEN_SECRET_KEY/")
  echo "$NEW_ENV_CONTENT" > "$ENV_FILE"
fi

source $ENV_FILE

export BACKEND_PORT=$BACKEND_PORT
export FRONTEND_PORT=$FRONTEND_PORT
export HTTPS_PORT=$HTTPS_PORT
export DATABASE_PORT=$DATABASE_PORT
export MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
export MYSQL_PASSWORD=$MYSQL_ROOT_PASSWORD
#sql

SQL_TEMPLATE_FILE="./mysql/my.cnf.template"
SQL_CONFIG_FILE="./mysql/my.cnf"
envsubst < $SQL_TEMPLATE_FILE > $SQL_CONFIG_FILE

#cert
if $CREATE_CERT; then
  CERT_FOLDER="nginx/certs"
  if [ ! -d "$CERT_FOLDER" ]; then
    echo "Folder doesn't exist，creating：$CERT_FOLDER"
    mkdir -p "$CERT_FOLDER"
    openssl genpkey -algorithm RSA -out nginx/certs/server.key
    openssl req -new -key nginx/certs/server.key -out nginx/certs/server.csr -config ssl.conf
    openssl x509 -req -days 365 -in nginx/certs/server.csr -signkey nginx/certs/server.key -out nginx/certs/server.crt
  else
    echo "Folder exist：$CERT_FOLDER"
  fi
fi

#nginx
NGINX_TEMPLATE_FILE="./nginx/nginx_template.conf"
NGINX_CONFIG_FILE="./nginx/nginx.conf"

if [ -z "$FRONTEND_PORT" ]; then
  echo "Error: FRONTEND_PORT not found in $ENV_FILE"
  exit 1
fi

sed -e "s/\${FRONTEND_PORT}/$FRONTEND_PORT/g" \
    -e "s/\${BACKEND_PORT}/$BACKEND_PORT/g" \
    -e "s/\${HTTPS_PORT}/$HTTPS_PORT/g" \
    $NGINX_TEMPLATE_FILE > $NGINX_CONFIG_FILE

#frontend
current_dir=$(pwd)
cd frontend || exit
npm run build
cd "$current_dir"

#backend
BACKEND_TEMPLATE_FILE="./backend/login_backend/config_template.yaml"
BACKEND_CONFIG_FILE="./backend/login_backend/config.yaml"

envsubst < $BACKEND_TEMPLATE_FILE > $BACKEND_CONFIG_FILE

docker compose up -d

echo "Frontend run at http://localhost:$FRONTEND_PORT"
echo "Backend run at http://localhost:$BACKEND_PORT"
echo "Database run at http://localhost:$BACKEND_PORT"
echo "Check api document at http://localhost:$BACKEND_PORT/redoc"
