from config import get_psycopg_connection
import random, datetime

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86399)
    return start + datetime.timedelta(days=random_days, seconds=random_seconds)

start_date = datetime.datetime(2025, 5, 1)
end_date = datetime.datetime(2025, 12, 31)

conn = get_psycopg_connection()
cur = conn.cursor()

cur.execute("SELECT account_id FROM accounts;")
account_ids = [row[0] for row in cur.fetchall()]

for _ in range(10):
    transaction_date = random_date(start_date, end_date)
    acc_from = random.choice(account_ids)
    acc_to = random.choice(account_ids)
    while acc_to == acc_from:
        acc_to = random.choice(account_ids)

    cur.execute("""
        INSERT INTO transactions (
            account_origin_id,
            account_destination_id,
            transaction_type_id,
            amount,
            transaction_date,
            branch_id,
            description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        acc_from,
        acc_to,
        random.randint(1, 4),
        round(random.uniform(10, 500), 2),
        transaction_date,
        random.randint(1, 10),
        'Auto-insert transaction'
    ))

conn.commit()
conn.close()
print("Inserted 10 new transactions.")
