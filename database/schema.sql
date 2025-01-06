CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE INDEX idx_email ON test_table(email);
