import random
import time
from datetime import date, timedelta
from config import get_psycopg_connection

conn = get_psycopg_connection()
cur = conn.cursor()

cur.execute("SELECT account_id FROM accounts;")
accounts = [r[0] for r in cur.fetchall()]

cur.execute("SELECT loan_status_id FROM loan_statuses;")
statuses = [r[0] for r in cur.fetchall()]

print("Auto loan generator started. Press Ctrl+C to stop.")

try:
    while True:
        acc = random.choice(accounts)
        status = random.choice(statuses)
        principal = round(random.uniform(1000, 10000), 2)
        rate = round(random.uniform(0.02, 0.15), 5)

        start_min = date(2023, 5, 1)
        start_max = date(2025, 5, 1)
        start = start_min + timedelta(days=random.randint(0, (start_max - start_min).days))
        
        end = start + timedelta(days=random.randint(180, 720))

        cur.execute("""
            INSERT INTO loans (
                account_id, loan_status_id, principal_amount,
                interest_rate, start_date, estimated_end_date
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (acc, status, principal, rate, start, end))

        conn.commit()
        print(f"Loan {principal}, {start}, {end} inserted.")
        time.sleep(10)
except KeyboardInterrupt:
    print("\nStopped.")
finally:
    cur.close()
    conn.close()
