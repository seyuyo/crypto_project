CREATE DATABASE crypto;

\c crypto

CREATE TABLE price_raw (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50),
    price DOUBLE PRECISION,
    timestamp TIMESTAMP
);

CREATE TABLE trend_stats (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(50),
    avg_1h DOUBLE PRECISION,
    avg_24h DOUBLE PRECISION,
    timestamp TIMESTAMP
);
