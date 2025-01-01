USE movies_api;

-- Create movies db

-- CREATE TABLE movies(
--     id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     genre VARCHAR(150) NOT NULL,
--     director VARCHAR(150) NOT NULL,
--     year YEAR NOT NULL,
--     RATING FLOAT NOT NULL
-- );

CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    passwd VARCHAR(60) NOT NULL
);

-- CREATE TABLE preferences(
--     user_id INT NOT NULL UNIQUE,
--     preferences JSON NOT NULL
-- );