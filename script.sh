#!/bin/bash
ENV_FILE="./.env"
ENV_SAMPLE_FILE="env_template"
source $ENV_FILE

export AUTH_SERVICE_PORT=$AUTH_SERVICE_PORT
export EXPENSE_SERVICE_PORT=$EXPENSE_SERVICE_PORT
export DATABASE_PORT=$DATABASE_PORT
export DOMAIN_NAME=$DOMAIN_NAME
export MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD
export MYSQL_PASSWORD=$MYSQL_ROOT_PASSWORD
export TOKEN_SECRET_KEY=$TOKEN_SECRET_KEY
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


sed -e "s/\${AUTH_SERVICE_PORT}/$AUTH_SERVICE_PORT/g" \
    -e "s/\${EXPENSE_SERVICE_PORT}/$EXPENSE_SERVICE_PORT/g" \
    -e "s/\${DOMAIN_NAME}/$DOMAIN_NAME/g" \
    $NGINX_TEMPLATE_FILE > $NGINX_CONFIG_FILE

#frontend
current_dir=$(pwd)
cd frontend || exit
npm run build
cd "$current_dir"

#backend
BACKEND_TEMPLATE_FILE="./backend/core/config/config_template.yaml"
BACKEND_CONFIG_FILE="./backend/core/config/config.yaml"

sed -e "s/\${MYSQL_PASSWORD}/$MYSQL_PASSWORD/g" \
    -e "s/\${DATABASE_PORT}/$DATABASE_PORT/g" \
    -e "s/\${TOKEN_SECRET_KEY}/$TOKEN_SECRET_KEY/g" \
    $BACKEND_TEMPLATE_FILE > $BACKEND_CONFIG_FILE

docker compose up -d

