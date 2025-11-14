import pandas as pd
from config import get_engine

engine = get_engine()

query = """
SELECT 
    DATE_TRUNC('month', transaction_date)::DATE AS month,
    COUNT(transaction_id) AS transaction_count
FROM transactions
GROUP BY month
ORDER BY month;
"""

df = pd.read_sql(query, engine)
df.to_csv("transaction_trends.csv", index=False)
print("CSV exported: transaction_trends.csv")