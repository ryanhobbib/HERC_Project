import sqlite3
import pandas as pd
import os
import time

### Query 1: Most common services
def common_services():
    # Connect to database
    conn = sqlite3.connect("data/medicare.db")

    # Run query
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
    df1.to_csv('outputs/result_csvs/top_services.csv', index=False)
    total_time = time.time() - start
    print("Query 1: Top 10 Services:")
    print(df1)
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    conn.close()
    return df1

### Query 2: Payment information by state
def payments_by_state():
    conn = sqlite3.connect("data/medicare.db")

    start = time.time()
    query = """
    SELECT
        provider_state,
        COUNT(DISTINCT npi) as num_providers,
        ROUND(AVG(avg_medicare_payment), 2) as avg_payment,
        ROUND(MIN(avg_medicare_payment), 2) as min_payment,
        ROUND(MAX(avg_medicare_payment), 2) as max_payment
    FROM medicare_payments
    WHERE hcpcs_code = '99214'
    GROUP BY provider_state
    ORDER BY avg_payment DESC
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv('outputs/result_csvs/payments_by_state.csv', index=False)
    total_time = time.time() - start
    print("Query 2: Payments by State")
    print(df)
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    # Close connection
    conn.close()
    return df

