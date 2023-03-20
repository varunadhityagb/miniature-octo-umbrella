CREATE DATABASE IF NOT EXISTS project_scam;
USE project_scam;

CREATE TABLE IF NOT EXISTS users(id INT AUTO_INCREMENT PRIMARY KEY,
								full_name VARCHAR(225),
                                email VARCHAR(225),
                                admin_access BOOLEAN, 
                                auth_key VARCHAR(225),
                                user_password VARCHAR(225));