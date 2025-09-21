-- Foreign Keys (format fk_<child>_<parent>)

-- accounts -> customers, account_types, account_statuses
ALTER TABLE accounts
  ADD CONSTRAINT fk_accounts_customers
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
      ON DELETE RESTRICT
      NOT VALID;

ALTER TABLE accounts
  ADD CONSTRAINT fk_accounts_account_types
    FOREIGN KEY (account_type_id) REFERENCES account_types(account_type_id)
      ON DELETE SET NULL
      NOT VALID;

ALTER TABLE accounts
  ADD CONSTRAINT fk_accounts_account_statuses
    FOREIGN KEY (account_status_id) REFERENCES account_statuses(account_status_id)
      ON DELETE SET NULL
      NOT VALID;

-- customers -> addresses, customer_types
ALTER TABLE customers
  ADD CONSTRAINT fk_customers_addresses
    FOREIGN KEY (address_id) REFERENCES addresses(address_id)
      ON DELETE SET NULL
      NOT VALID;

ALTER TABLE customers
  ADD CONSTRAINT fk_customers_customer_types
    FOREIGN KEY (customer_type_id) REFERENCES customer_types(customer_type_id)
      ON DELETE SET NULL
      NOT VALID;

-- branches -> addresses
ALTER TABLE branches
  ADD CONSTRAINT fk_branches_addresses
    FOREIGN KEY (address_id) REFERENCES addresses(address_id)
      ON DELETE SET NULL
      NOT VALID;

-- loans -> accounts, loan_statuses
ALTER TABLE loans
  ADD CONSTRAINT fk_loans_accounts
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
      ON DELETE RESTRICT
      NOT VALID;

ALTER TABLE loans
  ADD CONSTRAINT fk_loans_loan_statuses
    FOREIGN KEY (loan_status_id) REFERENCES loan_statuses(loan_status_id)
      ON DELETE SET NULL
      NOT VALID;

-- transactions -> accounts (origin & destination), transaction_types, branches
ALTER TABLE transactions
  ADD CONSTRAINT fk_transactions_account_origin
    FOREIGN KEY (account_origin_id) REFERENCES accounts(account_id)
      ON DELETE SET NULL
      NOT VALID;

ALTER TABLE transactions
  ADD CONSTRAINT fk_transactions_account_destination
    FOREIGN KEY (account_destination_id) REFERENCES accounts(account_id)
      ON DELETE SET NULL
      NOT VALID;

ALTER TABLE transactions
  ADD CONSTRAINT fk_transactions_transaction_types
    FOREIGN KEY (transaction_type_id) REFERENCES transaction_types(transaction_type_id)
      ON DELETE SET NULL
      NOT VALID;

ALTER TABLE transactions
  ADD CONSTRAINT fk_transactions_branches
    FOREIGN KEY (branch_id) REFERENCES branches(branch_id)
      ON DELETE SET NULL
      NOT VALID;