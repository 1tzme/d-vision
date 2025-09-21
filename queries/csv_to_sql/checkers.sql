-- checkers for finding records that reference non-existent parent strings

-- accounts with no customer_id
SELECT a.account_id, a.customer_id
FROM accounts a
LEFT JOIN customers c ON a.customer_id = c.customer_id
WHERE a.customer_id IS NOT NULL AND c.customer_id IS NULL
LIMIT 20;

-- transactions with non existent account_origin_id
SELECT t.transaction_id, t.account_origin_id
FROM transactions t
LEFT JOIN accounts a ON t.account_origin_id = a.account_id
WHERE t.account_origin_id IS NOT NULL AND a.account_id IS NULL LIMIT 20;
