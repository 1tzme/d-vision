from dotenv import load_dotenv
import os
import psycopg2
import csv

# laod variables from .env
load_dotenv()

# connection to db
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST")
)
cur = conn.cursor()

def run_query(query, filename):
    cur.execute(query)
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    # output in terminal
    print(f"\n=== {filename} ===")
    for row in rows:
        print(row)

    # save to csv
    with open(f"{filename}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colnames)
        writer.writerows(rows)

# num of customers
query1 = "SELECT COUNT(*) AS customers_count FROM customers;"

# average balance by account type
query2 = """
SELECT account_type_id, AVG(balance) AS avg_balance
    FROM accounts
    GROUP BY account_type_id
"""

# number of credits by status (#2 in queries/testing/queries.sql)
query3 = """
SELECT ls.loan_status_id,
    ls.status_name,
    COUNT(l.loan_id) AS loans_count,
    SUM(l.principal_amount)::numeric(18,2) AS loans_sum
FROM loans l
LEFT JOIN loan_statuses ls ON l.loan_status_id = ls.loan_status_id
GROUP BY ls.loan_status_id, ls.status_name
ORDER BY loans_count DESC;
"""

# top 10 customers by number of transactions (#8 in queries/testing/queries.sql)
query4 = """
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
"""

query5 = """
SELECT account_types.account_type_id,
       account_types.type_name,
       AVG(a.balance)::numeric(18,2) AS avg_balance,
       COUNT(a.account_id) AS accounts_count
FROM accounts a
LEFT JOIN account_types account_types ON a.account_type_id = account_types.account_type_id
GROUP BY account_types.account_type_id, account_types.type_name
ORDER BY avg_balance DESC;
"""

query6 = """
SELECT to_char(date_trunc('month', t.transaction_date), 'YYYY-MM') AS year_month,
       COUNT(*) AS tx_count,
       SUM(t.amount)::numeric(18,2) AS tx_sum
FROM transactions t
WHERE t.transaction_date >= date_trunc('month', CURRENT_DATE) - INTERVAL '11 months'
GROUP BY 1
ORDER BY 1;
"""

query7 = """
SELECT tt.transaction_type_id,
       tt.type_name,
       COUNT(t.transaction_id) AS tx_count,
       AVG(t.amount)::numeric(18,2) AS avg_amount,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY t.amount)::numeric(18,2) AS median_amount
FROM transactions t
LEFT JOIN transaction_types tt ON t.transaction_type_id = tt.transaction_type_id
GROUP BY tt.transaction_type_id, tt.type_name
ORDER BY avg_amount DESC;
"""

query8 = """
SELECT c.customer_id,
       COALESCE(c.first_name || ' ' || c.last_name, c.customer_id::text) AS customer_name,
       COUNT(a.account_id) AS accounts_count,
       SUM(a.balance)::numeric(18,2) AS total_balance
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, customer_name
HAVING COUNT(a.account_id) > 1
ORDER BY total_balance DESC;
"""

query9 = """
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
"""

query10 = """
SELECT at.type_name,
       COUNT(a.account_id) AS accounts_count,
       AVG(a.balance) AS avg_balance,
       MIN(a.balance) AS min_balance,
       MAX(a.balance) AS max_balance
FROM accounts a
JOIN account_types at ON a.account_type_id = at.account_type_id
GROUP BY at.type_name
ORDER BY avg_balance DESC;
"""

query11 = """
SELECT ls.status_name,
       COUNT(l.loan_id) AS loans_count,
       SUM(l.principal_amount) AS total_principal,
       AVG(l.principal_amount) AS avg_principal
FROM loans l
JOIN loan_statuses ls ON l.loan_status_id = ls.loan_status_id
GROUP BY ls.status_name
ORDER BY loans_count DESC;
"""

run_query(query1, "customer_count")
run_query(query2, "avg_balance_per_acc_type")
run_query(query3, "loans_stats")
run_query(query4, "top10_customer_transactions")
run_query(query5, "test1")
run_query(query6, "test2")
run_query(query7, "test3")
run_query(query8, "test4")
run_query(query9, "test5")
run_query(query10, "test6")
run_query(query11, "test7")

cur.close()
conn.close()