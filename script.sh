#nginx
ENV_FILE="./.env"
NGINX_TEMPLATE_FILE="./nginx/nginx_template.conf"
NGINX_CONFIG_FILE="./nginx/nginx.conf"

source $ENV_FILE

if [ -z "$FRONTEND_PORT" ]; then
  echo "Error: FRONTEND_PORT not found in $ENV_FILE"
  exit 1
fi

sed "s/\${FRONTEND_PORT}/$FRONTEND_PORT/g" $NGINX_TEMPLATE_FILE > $NGINX_CONFIG_FILE

echo "New Nginx config file generated: $FRONTEND_PORT"

