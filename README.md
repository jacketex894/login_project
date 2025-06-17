# login-project

This project helps me learn how to build full-stack applications by connecting a frontend with backend services, working with databases, and implementing user registration and login flows.

It features a frontend, an auth-service, an expense-service, and a database, all orchestrated using Docker Compose.

On the backend, I used a microservices approach with MVC structure and implemented JWT authentication for secure access control.


## Technology Stack
* Frontend: Vue.js, Vite, Vuetify
* Backend: FastAPI
* Database: MySQL
* Database Operations: SQLAlchemy
* Web Server: Nginx
* Containerization: Docker, Docker Compose
* PacPackage Management: Poetry

## Installation and Setup
1. Prerequisites
    * Install Docker
      * Please check [Docker Docs](https://docs.docker.com/engine/install/ubuntu/)
    * Install npm
      * Command: `npm install -g npm` 
      * Required for build frontend.
    * Install openssl (Optional) 
      * Command: `sudo apt install openssl`
      * Required for generating a self-signed SSL certificate.
      * If you set `CREATE_CERT = false` in the config, you don't need to install openssl, but you will need to provide another certificate for HTTPS.
2. Configuration Setup

   You need to set up environment variables in the .env file.
   
   You can either create it manually based on the env_template or let the script generate it for you.
   Run the following command:
    ```
    ./gen_env.sh
    ```
    * .env file:
    ```
    AUTH_SERVICE_PORT= 
    EXPENSE_SERVICE_PORT=
    DATABASE_PORT=
    DOMAIN_NAME=(default is local.test)
    MYSQL_ROOT_PASSWORD=
    CREATE_CERT=(default is true)
    TOKEN_SECRET_KEY=
    ```

    Use AUTH_SERVICE_PORT,EXPENSE_SERVICE_PORT as backend service port.

    Use DATABASE_PORT as database port.

    Use DOMAIN_NAME as your web application domain name.

    * In windows you need to add `127.0.0.1 local.test`to C:\Windows\System32\drivers\etc\hosts if you want to activate on local.

    Use MYSQL_ROOT_PASSWORD as your mysql db password.
    
    CREATE_CERT need to be true if you don't have certificates for https. 

    TOKEN_SECRET_KEY use for encrypt jwt token.

3. Start the Service
    Run the following command:
    ```
    ./script.sh
    ```
    This script will:
   
   * Generate SQL settings based on `.env`.
   * Generate the SSL certificate if `CREATE_CERT=true`.
   * Generate Nginx settings based on `.env`.
   * Build the frontend for Nginx.
   * Generate backend setting base on `.env`.
   * Start the following containers in the background:
      * Nginx (Reverse Proxy and Frontend Service)
      * MySQL Database
      * auth-service
      * expense-service

## Access the Application
After running the script, you can access the application by navigating to the URL `https://local.test`.
   
## Note: 
If `CREATE_CERT=true`, you may see a "Your connection is not private" warning in your browser. 

This happens because the certificate is self-signed, rather than being issued by a trusted certificate authority (CA).

##  Configure Nginx to Enforce HTTPS
Nginx is set to automatically redirect all incoming HTTP requests to HTTPS. Make sure you have valid SSL certificates, or use self-signed certificates if you are working in a development environment.
