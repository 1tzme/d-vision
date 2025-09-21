-- 4b. basic queries
SELECT * FROM customers LIMIT 10;

SELECT * FROM transactions 
WHERE amount > 1000 
ORDER BY transaction_date DESC 
LIMIT 10;

SELECT c.customer_id, c.first_name, a.account_id, t.amount
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
JOIN transactions t ON a.account_id = t.account_origin_id
LIMIT 10;