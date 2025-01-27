CREATE DATABASE PTCAO;

CREATE TABLE users (
    account_id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE BusinessRegistration (
    business_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    business_registration_no VARCHAR(100) NOT NULL,
    business_name VARCHAR(255) NOT NULL,
    official_contact_no VARCHAR(50) NOT NULL,
    business_address VARCHAR(255) NOT NULL,
    taxpayer_name VARCHAR(255) NOT NULL,
    total_employees INTEGER NOT NULL,
    total_rooms INTEGER NOT NULL,
    total_beds INTEGER NOT NULL,
    CONSTRAINT fk_account FOREIGN KEY (account_id) REFERENCES users(account_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);


