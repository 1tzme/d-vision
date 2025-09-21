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
    password=os.getenv("USER_PASSWORD"),
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

run_query(query1, "customer_count")
run_query(query2, "avg_balance_per_acc_type")
run_query(query3, "loans_stats")
run_query(query4, "top10_customer_transactions")

cur.close()
conn.close()