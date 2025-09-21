-- reference tables
INSERT INTO account_statuses (account_status_id, status_name)
SELECT raw.safe_int(AccountStatusID), NULLIF(trim(StatusName),'')
FROM raw.account_statuses_raw
WHERE raw.safe_int(AccountStatusID) IS NOT NULL
ON CONFLICT (account_status_id) DO NOTHING;

INSERT INTO account_types (account_type_id, type_name)
SELECT raw.safe_int(AccountTypeID), NULLIF(trim(TypeName),'')
FROM raw.account_types_raw
WHERE raw.safe_int(AccountTypeID) IS NOT NULL
ON CONFLICT (account_type_id) DO NOTHING;

INSERT INTO customer_types (customer_type_id, type_name)
SELECT raw.safe_int(CustomerTypeID), NULLIF(trim(TypeName),'')
FROM raw.customer_types_raw
WHERE raw.safe_int(CustomerTypeID) IS NOT NULL
ON CONFLICT (customer_type_id) DO NOTHING;

INSERT INTO transaction_types (transaction_type_id, type_name)
SELECT raw.safe_int(TransactionTypeID), NULLIF(trim(TypeName),'')
FROM raw.transaction_types_raw
WHERE raw.safe_int(TransactionTypeID) IS NOT NULL
ON CONFLICT (transaction_type_id) DO NOTHING;

INSERT INTO loan_statuses (loan_status_id, status_name)
SELECT raw.safe_int(LoanStatusID), NULLIF(trim(StatusName),'')
FROM raw.loan_statuses_raw
WHERE raw.safe_int(LoanStatusID) IS NOT NULL
ON CONFLICT (loan_status_id) DO NOTHING;

-- addresses, branches, customers
INSERT INTO addresses (address_id, street, city, country)
SELECT raw.safe_int(AddressID), NULLIF(trim(Street),''), NULLIF(trim(City),''), NULLIF(trim(Country),'')
FROM raw.addresses_raw
WHERE raw.safe_int(AddressID) IS NOT NULL
ON CONFLICT (address_id) DO NOTHING;

INSERT INTO branches (branch_id, branch_name, address_id)
SELECT raw.safe_int(BranchID), NULLIF(trim(BranchName),''), raw.safe_int(AddressID)
FROM raw.branches_raw
WHERE raw.safe_int(BranchID) IS NOT NULL
ON CONFLICT (branch_id) DO NOTHING;

INSERT INTO customers (customer_id, first_name, last_name, date_of_birth, address_id, customer_type_id)
SELECT
  raw.safe_int(CustomerID),
  NULLIF(trim(FirstName),''),
  NULLIF(trim(LastName),''),
  raw.safe_date(DateOfBirth),
  raw.safe_int(AddressID),
  raw.safe_int(CustomerTypeID)
FROM raw.customers_raw
WHERE raw.safe_int(CustomerID) IS NOT NULL
ON CONFLICT (customer_id) DO NOTHING;

-- accounts, loans, transactions
INSERT INTO accounts (account_id, customer_id, account_type_id, account_status_id, balance, opening_date)
SELECT
  raw.safe_int(AccountID),
  raw.safe_int(CustomerID),
  raw.safe_int(AccountTypeID),
  raw.safe_int(AccountStatusID),
  raw.safe_numeric(Balance),
  raw.safe_date(OpeningDate)
FROM raw.accounts_raw
WHERE raw.safe_int(AccountID) IS NOT NULL
ON CONFLICT (account_id) DO NOTHING;

INSERT INTO loans (loan_id, account_id, loan_status_id, principal_amount, interest_rate, start_date, estimated_end_date)
SELECT
  raw.safe_int(LoanID),
  raw.safe_int(AccountID),
  raw.safe_int(LoanStatusID),
  raw.safe_numeric(PrincipalAmount),
  raw.safe_numeric(InterestRate),
  raw.safe_date(StartDate),
  raw.safe_date(EstimatedEndDate)
FROM raw.loans_raw
WHERE raw.safe_int(LoanID) IS NOT NULL
ON CONFLICT (loan_id) DO NOTHING;

INSERT INTO transactions (transaction_id, account_origin_id, account_destination_id, transaction_type_id, amount, transaction_date, branch_id, description)
SELECT
  raw.safe_int(TransactionID),
  raw.safe_int(AccountOriginID),
  raw.safe_int(AccountDestinationID),
  raw.safe_int(TransactionTypeID),
  raw.safe_numeric(Amount),
  raw.safe_timestamp(TransactionDate),
  raw.safe_int(BranchID),
  NULLIF(trim(Description),'')
FROM raw.transactions_raw
WHERE raw.safe_int(TransactionID) IS NOT NULL
ON CONFLICT (transaction_id) DO NOTHING;
