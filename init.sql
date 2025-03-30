BEGIN;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS wallet_requests (
    uuid uuid DEFAULT uuid_generate_v4() NOT NULL,
    address VARCHAR,
    balance DOUBLE PRECISION,
    bandwidth INTEGER,
    energy INTEGER,
    date_created TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT wallet_requests_pk PRIMARY KEY (uuid)
);

COMMIT;