import sqlite3
import pandas as pd
import os
import time

# Connect to database
conn = sqlite3.connect("data/medicare.db")

# Query 1: Most common services
start = time.time()
query1 = """
SELECT 
    hcpcs_code,
    hcpcs_description,
    SUM(total_services) AS total_services_count,
    ROUND(AVG(avg_medicare_payment), 2) AS avg_payment, 
    COUNT(DISTINCT npi) AS num_providers
FROM medicare_payments
WHERE hcpcs_code IS NOT NULL
GROUP BY hcpcs_code, hcpcs_description
ORDER BY total_services_count DESC
LIMIT 10
"""
df1 = pd.read_sql_query(query1, conn)
df1.to_csv('outputs/result_csvs/01_top_services.csv', index=False)
total_time = time.time() - start
print("Query 1: Top 10 Services:")
print(df1)
print(f"Query time: {total_time:.2f} seconds")
print("\n")

# Close connection
conn.close()

