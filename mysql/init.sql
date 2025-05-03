CREATE DATABASE user_db;
USE user_db;
CREATE TABLE members(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255)  UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    mail VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_ip VARCHAR(45)
);

CREATE DATABASE item_db;
USE item_db;
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    category TEXT
);

CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL REFERENCES items(id),
    quantity INT NOT NULL,
    amount INT NOT NULL,
    purchase_date DATE NOT NULL,
    expiration_date DATE,
    note TEXT
);

CREATE TABLE usages (
    id SERIAL PRIMARY KEY,
    item_id INT NOT NULL REFERENCES items(id),
    quantity FLOAT NOT NULL,
    usage_date DATE NOT NULL,
    purpose TEXT
);