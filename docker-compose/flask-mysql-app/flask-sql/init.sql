CREATE DATABASE IF NOT EXISTS myapp;
USE myapp;
CREATE TABLE greetings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(250) NOT NULL
);
INSERT INTO greetings (message) VALUES ('Hello from Flask + MySQL!');
