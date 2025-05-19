CREATE DATABASE user_db ;
USE user_db ;
CREATE TABLE members(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255)  UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    mail VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_ip VARCHAR(45)
);
CREATE TABLE transactions (
    transaction_id INT  AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category VARCHAR(100),
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    total_cost FLOAT NOT NULL,
    pay_by VARCHAR(255) NOT NULL DEFAULT 'cash',
    date DATETIME NOT NULL
);