-- 1) Average balance by account type
-- Displays the account type name and average balance for each type.
SELECT account_types.account_type_id,
       account_types.type_name,
       AVG(a.balance)::numeric(18,2) AS avg_balance,
       COUNT(a.account_id) AS accounts_count
FROM accounts a
LEFT JOIN account_types account_types ON a.account_type_id = account_types.account_type_id
GROUP BY account_types.account_type_id, account_types.type_name
ORDER BY avg_balance DESC;

-- 2) Number of credits by status
-- Shows the number of credits and the total amount of credits for each credit status.
SELECT ls.loan_status_id,
       ls.status_name,
       COUNT(l.loan_id) AS loans_count,
       SUM(l.principal_amount)::numeric(18,2) AS loans_sum
FROM loans l
LEFT JOIN loan_statuses ls ON l.loan_status_id = ls.loan_status_id
GROUP BY ls.loan_status_id, ls.status_name
ORDER BY loans_count DESC;

-- 3) Monthly transaction volume (amount) for the last 12 months
-- Displays the year-month and total amount/number of transactions.
SELECT to_char(date_trunc('month', t.transaction_date), 'YYYY-MM') AS year_month,
       COUNT(*) AS tx_count,
       SUM(t.amount)::numeric(18,2) AS tx_sum
FROM transactions t
WHERE t.transaction_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '11 months'
GROUP BY 1
ORDER BY 1;

-- 4) Average transaction size by transaction type
-- Uses aggregate for average and percentile_cont for median.
SELECT tt.transaction_type_id,
       tt.type_name,
       COUNT(t.transaction_id) AS tx_count,
       AVG(t.amount)::numeric(18,2) AS avg_amount,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY t.amount)::numeric(18,2) AS median_amount
FROM transactions t
LEFT JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
GROUP BY tt.transaction_type_id, tt.type_name
ORDER BY avg_amount DESC;

-- 5) Customers with multiple accounts: number of accounts and total balance
-- Shows customers who have more than one account and sorts them by total balance.
SELECT c.customer_id,
       COALESCE(c.first_name || ' ' || c.last_name, c.customer_id::text) AS customer_name,
       COUNT(a.account_id) AS accounts_count,
       SUM(a.balance)::numeric(18,2) AS total_balance
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, customer_name
HAVING COUNT(a.account_id) > 1
ORDER BY total_balance DESC;

-- 6) Active accounts with a negative balance (possible overdraft)
-- We assume that account_statuses contains the status name (‘active’ or similar).
SELECT a.account_id,
       a.customer_id,
       COALESCE(c.first_name || ' ' || c.last_name, c.customer_id::text) AS customer_name,
       a.balance::numeric(18,2) AS balance,
       ast.status_name
FROM accounts a
LEFT JOIN account_statuses ast ON a.account_status_id = ast.account_status_id
LEFT JOIN customers c ON a.customer_id = c.customer_id
WHERE a.balance < 0
  AND LOWER(ast.status_name) IN ('active', 'opened', 'open')
ORDER BY a.balance ASC;

-- 7) Average balance by account type
-- Description: calculates the number of accounts and balance statistics for each account type.
SELECT at.type_name,
       COUNT(a.account_id) AS accounts_count,
       AVG(a.balance) AS avg_balance,
       MIN(a.balance) AS min_balance,
       MAX(a.balance) AS max_balance
FROM accounts a
JOIN account_types at ON a.account_type_id = at.account_type_id
GROUP BY at.type_name
ORDER BY avg_balance DESC;

-- 8) Top 10 customers by number of transactions (both sent and received)
-- Description: we take into account transactions where any customer account is the source or recipient.
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       COUNT(t.transaction_id) AS transactions_count
FROM customers c
JOIN accounts a ON a.customer_id = c.customer_id
JOIN transactions t ON (t.account_origin_id = a.account_id OR t.account_destination_id = a.account_id)
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY transactions_count DESC
LIMIT 10;

-- 9) Number of loans by status
-- Description: number and total/average amount of loans for each status.
SELECT ls.status_name,
       COUNT(l.loan_id) AS loans_count,
       SUM(l.principal_amount) AS total_principal,
       AVG(l.principal_amount) AS avg_principal
FROM loans l
JOIN loan_statuses ls ON l.loan_status_id = ls.loan_status_id
GROUP BY ls.status_name
ORDER BY loans_count DESC;

-- 10) Top 5 branches by total transaction volume (by absolute amount)
-- Description: sums up the transaction volume by branch and shows the top 5 by total_volume.
SELECT b.branch_id, b.branch_name,
       COUNT(t.transaction_id) AS txn_count,
       SUM(ABS(t.amount)) AS total_volume
FROM transactions t
JOIN branches b ON t.branch_id = b.branch_id
GROUP BY b.branch_id, b.branch_name
ORDER BY total_volume DESC
LIMIT 5;

-- 11) Top 50 large transfers (transaction_type = ‘transfer’ or similar)
-- Description: selects transactions of type transfer/wire/payment and returns the 50 largest in absolute amount.
SELECT t.transaction_id,
       t.account_origin_id,
       t.account_destination_id,
       tt.type_name AS transaction_type,
       t.amount,
       t.transaction_date,
       b.branch_name
FROM transactions t
LEFT JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
LEFT JOIN branches b ON t.branch_id = b.branch_id
WHERE tt.type_name ILIKE '%transfer%' OR tt.type_name ILIKE '%wire%' OR tt.type_name ILIKE '%payment%'
ORDER BY ABS(t.amount) DESC
LIMIT 50;