-- In terminal
-- psql < air_traffic.sql  (Mac)
-- psql -f medical_center.sql (PC)


DROP DATABASE IF EXISTS mars_db;

CREATE DATABASE mars_db;

\c mars_db


CREATE TABLE photos (
    id SERIAL PRIMARY KEY,
    rover_name TEXT NOT NULL,
    earth_date DATE NOT NULL,
    sol INTEGER NOT NULL,
    urls TEXT
  
);




INSERT INTO photos
    (rover_name, earth_date, sol, urls)
VALUES
    ('Curiosity', '2021-01-01', 1, 'https://images.unsplash.com/photo-1573588028698-f4759befb09a?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=890&q=80');
  


    -- ('Curiosity'),
    -- ('Insight'),
    -- ('Spirit'),
    -- ('Perseverance');