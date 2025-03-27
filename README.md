# login-project

This project is designed to help me learn how to set up frontend-backend communication, handle database operations, and understand the registration and login processes. It includes a frontend, backend, and a database, all managed and started via Docker Compose.

Note: This project is still under development, and currently, only the registration functionality is complete.

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
    You need to set up environment variables in the .env file. You can either create it manually based on the env_template or let the script generate it for you.
    * .env file:
    ```
    BACKEND_PORT= 
    FRONTEND_PORT=
    DATABASE_PORT=
    MYSQL_ROOT_PASSWORD=
    CREATE_CERT=
    ```

3. Start the Service
    Run the following command:
    ```
    ./script.sh
    ```
    This script will:
       * Create the `.env` file if it doesn’t exist.
       * Generate SQL settings based on `.env`.
       * Generate the SSL certificate if `CREATE_CERT=true`.
       * Generate Nginx settings based on `.env`.
       * Build the frontend for Nginx.
       * Generate backend setting base on `.env`.
       * Start the following containers in the background:
         * Nginx (Reverse Proxy and Frontend Service)
         * MySQL Database
         * Backend FastAPI service
       * Display the following URLs:
         * Frontend
         * Backend
         * Database
         * API Documentation

## Access the Application
After running the script, you can access the application by navigating to the URLs displayed by the script in your browser.
   
## Note: 
If `CREATE_CERT=true`, you may see a "Your connection is not private" warning in your browser. This happens because the certificate is self-signed, rather than being issued by a trusted certificate authority (CA).

##  Configure Nginx to Enforce HTTPS
Nginx is set to automatically redirect all incoming HTTP requests to HTTPS. Make sure you have valid SSL certificates, or use self-signed certificates if you are working in a development environment.