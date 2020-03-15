DROP TABLE IF EXISTS time_series;
DROP TABLE IF EXISTS stock_meta_data;
DROP TABLE IF EXISTS black_listed_symbols;

CREATE TABLE time_series
(
    id INTEGER PRIMARY KEY,
    Date TEXT NOT NULL,
    Price REAL NOT NULL,
    Symbol TEXT NOT NULL,
    FOREIGN KEY
    (Symbol) REFERENCES stock_meta_data
    (Symbol)
);

CREATE TABLE stock_meta_data
(
    id INTEGER PRIMARY KEY,
    Symbol TEXT NOT NULL,
    Name TEXT NOT NULL,
    Sector TEXT NOT NULL
);

CREATE TABLE black_listed_symbols
(
    id INTEGER PRIMARY KEY,
    Symbol TEXT NOT NULL
); 