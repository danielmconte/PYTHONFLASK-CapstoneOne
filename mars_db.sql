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
    urls TEXT,
    user_id = INTEGER
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)




INSERT INTO photos
    (rover_name, earth_date, sol, urls, user_id)
VALUES
('curiosity', '2014-01-07', 506, 'http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00506/opgs/edr/fcam/FLB_442416860EDR_F0250242FHAZ00304M_.JPG', 1),
('perseverance', '2021-02-20',2, 'https://mars.nasa.gov/mars2020-raw-images/pub/ods/surface/sol/00002/ids/edr/browse/edl/EDF_0002_0667110740_696ECV_N0010052EDLC00002_0010LUJ01_1200.jpg', 2),
('curiosity', '2012-10-06', 60, 'http://mars.jpl.nasa.gov/msl-raw-images/proj/msl/redops/ods/surface/sol/00060/opgs/edr/fcam/FRA_402822752EDR_F0050104FHAZ00202M_.JPG', 2);
 
INSERT INTO users
    (username, password)
VALUES
('bluethecat', 'iamcat123')
('mrmonkey', 'bananaslol')


