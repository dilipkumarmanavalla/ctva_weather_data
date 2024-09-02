\connect weather_db;

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    max_temp INTEGER,
    min_temp INTEGER,
    precipitation INTEGER,
    UNIQUE (station_id, date)
);

CREATE TABLE weather_stats (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50) NOT NULL,
    year INTEGER NOT NULL,
    avg_max_temp FLOAT,
    avg_min_temp FLOAT,
    total_precipitation FLOAT,
    UNIQUE (station_id, year)
);

