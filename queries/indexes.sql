-- INDEXES
CREATE INDEX IF NOT EXISTS idx_accounts_customer_id ON accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_accounts_account_type_id ON accounts(account_type_id);
CREATE INDEX IF NOT EXISTS idx_accounts_account_status_id ON accounts(account_status_id);
CREATE INDEX IF NOT EXISTS idx_accounts_opening_date ON accounts(opening_date);

CREATE INDEX IF NOT EXISTS idx_customers_address_id ON customers(address_id);
CREATE INDEX IF NOT EXISTS idx_customers_customer_type_id ON customers(customer_type_id);
CREATE INDEX IF NOT EXISTS idx_customers_dob ON customers(date_of_birth);

CREATE INDEX IF NOT EXISTS idx_branches_address_id ON branches(address_id);

CREATE INDEX IF NOT EXISTS idx_loans_account_id ON loans(account_id);
CREATE INDEX IF NOT EXISTS idx_loans_loan_status_id ON loans(loan_status_id);
CREATE INDEX IF NOT EXISTS idx_loans_start_date ON loans(start_date);
CREATE INDEX IF NOT EXISTS idx_loans_estimated_end_date ON loans(estimated_end_date);

CREATE INDEX IF NOT EXISTS idx_transactions_account_origin_id ON transactions(account_origin_id);
CREATE INDEX IF NOT EXISTS idx_transactions_account_destination_id ON transactions(account_destination_id);
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_type_id ON transactions(transaction_type_id);
CREATE INDEX IF NOT EXISTS idx_transactions_branch_id ON transactions(branch_id);
CREATE INDEX IF NOT EXISTS idx_transactions_transaction_date ON transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_transactions_amount ON transactions(amount);

-- Indexes for reference guides
CREATE INDEX IF NOT EXISTS idx_account_types_type_name ON account_types(type_name);
CREATE INDEX IF NOT EXISTS idx_account_statuses_status_name ON account_statuses(status_name);
CREATE INDEX IF NOT EXISTS idx_customer_types_type_name ON customer_types(type_name);
CREATE INDEX IF NOT EXISTS idx_transaction_types_type_name ON transaction_types(type_name);
CREATE INDEX IF NOT EXISTS idx_loan_statuses_status_name ON loan_statuses(status_name);
