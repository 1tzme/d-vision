CREATE TABLE raw.account_statuses_raw (
  AccountStatusID TEXT,
  StatusName      TEXT
);

CREATE TABLE raw.account_types_raw (
  AccountTypeID TEXT,
  TypeName      TEXT
);

CREATE TABLE raw.accounts_raw (
  AccountID       TEXT,
  CustomerID      TEXT,
  AccountTypeID   TEXT,
  AccountStatusID TEXT,
  Balance         TEXT,
  OpeningDate     TEXT
);

CREATE TABLE raw.addresses_raw (
  AddressID TEXT,
  Street    TEXT,
  City      TEXT,
  Country   TEXT
);

CREATE TABLE raw.branches_raw (
  BranchID   TEXT,
  BranchName TEXT,
  AddressID  TEXT
);

CREATE TABLE raw.customer_types_raw (
  CustomerTypeID TEXT,
  TypeName       TEXT
);

CREATE TABLE raw.customers_raw (
  CustomerID     TEXT,
  FirstName      TEXT,
  LastName       TEXT,
  DateOfBirth    TEXT,
  AddressID      TEXT,
  CustomerTypeID TEXT
);

CREATE TABLE raw.loan_statuses_raw (
  LoanStatusID TEXT,
  StatusName   TEXT
);

CREATE TABLE raw.loans_raw (
  LoanID           TEXT,
  AccountID        TEXT,
  LoanStatusID     TEXT,
  PrincipalAmount  TEXT,
  InterestRate     TEXT,
  StartDate        TEXT,
  EstimatedEndDate TEXT
);

CREATE TABLE raw.transaction_types_raw (
  TransactionTypeID TEXT,
  TypeName          TEXT
);

CREATE TABLE raw.transactions_raw (
  TransactionID         TEXT,
  AccountOriginID       TEXT,
  AccountDestinationID  TEXT,
  TransactionTypeID     TEXT,
  Amount                TEXT,
  TransactionDate       TEXT,
  BranchID              TEXT,
  Description           TEXT
);
