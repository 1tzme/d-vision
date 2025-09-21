CREATE TABLE IF NOT EXISTS account_statuses (
  account_status_id INTEGER PRIMARY KEY,
  status_name       TEXT
);

CREATE TABLE IF NOT EXISTS account_types (
  account_type_id INTEGER PRIMARY KEY,
  type_name       TEXT
);

CREATE TABLE IF NOT EXISTS customer_types (
  customer_type_id INTEGER PRIMARY KEY,
  type_name        TEXT
);

CREATE TABLE IF NOT EXISTS addresses (
  address_id INTEGER PRIMARY KEY,
  street     TEXT,
  city       TEXT,
  country    TEXT
);

CREATE TABLE IF NOT EXISTS branches (
  branch_id   INTEGER PRIMARY KEY,
  branch_name TEXT,
  address_id  INTEGER
);

CREATE TABLE IF NOT EXISTS transaction_types (
  transaction_type_id INTEGER PRIMARY KEY,
  type_name           TEXT
);

CREATE TABLE IF NOT EXISTS loan_statuses (
  loan_status_id INTEGER PRIMARY KEY,
  status_name    TEXT
);

-- dependent tables (customers, accounts, loans, transactions)
CREATE TABLE IF NOT EXISTS customers (
  customer_id     INTEGER PRIMARY KEY,
  first_name      TEXT,
  last_name       TEXT,
  date_of_birth   DATE,
  address_id      INTEGER,
  customer_type_id INTEGER
);

CREATE TABLE IF NOT EXISTS accounts (
  account_id       INTEGER PRIMARY KEY,
  customer_id      INTEGER,
  account_type_id  INTEGER,
  account_status_id INTEGER,
  balance          NUMERIC(14,2),
  opening_date     DATE
);

CREATE TABLE IF NOT EXISTS loans (
  loan_id            INTEGER PRIMARY KEY,
  account_id         INTEGER,
  loan_status_id     INTEGER,
  principal_amount   NUMERIC(14,2),
  interest_rate      NUMERIC(7,5),
  start_date         DATE,
  estimated_end_date DATE
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id        INTEGER PRIMARY KEY,
  account_origin_id     INTEGER,
  account_destination_id INTEGER,
  transaction_type_id   INTEGER,
  amount                NUMERIC(14,2),
  transaction_date      TIMESTAMP,
  branch_id             INTEGER,
  description           TEXT
);
