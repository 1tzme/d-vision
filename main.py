from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("USER_PASSWORD"),
    host=os.getenv("DB_HOST")
)
cur = conn.cursor()

# query example
cur.execute("SELECT COUNT(*) FROM customers;")
print("Customers:", cur.fetchone()[0],'\n')

# another query example
cur.execute("""
    SELECT account_type_id, AVG(balance) 
    FROM accounts 
    GROUP BY account_type_id
""")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()