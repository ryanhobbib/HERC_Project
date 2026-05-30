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
    query = """
    SELECT
        hcpcs_code,
        MAX(hcpcs_description) AS hcpcs_description,
        SUM(total_services) AS total_services,
        ROUND(AVG(avg_medicare_payment), 2) AS avg_payment
    FROM medicare_payments
    WHERE hcpcs_code IS NOT NULL AND total_services > 1000
    GROUP BY hcpcs_code
    ORDER BY total_services DESC
    LIMIT 10;
    """

    df1 = pd.read_sql_query(query, conn)
    df1.to_csv('outputs/result_csvs/common_services.csv', index=False)
    total_time = time.time() - start
    print("Query 1: Most Common Services:")
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    conn.close()
    return df1

### Query 2: Payment information for standard outpatient visit by state
def outpatient_visit_payments_by_state():
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
    df.to_csv('outputs/result_csvs/outpatient_visit_payments_by_state.csv', index=False)
    total_time = time.time() - start
    print("Query 2: Outpatient Visit Payments by State")
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    # Close connection
    conn.close()
    return df

### Query 3: Payment information by specialty
def payments_by_specialty():
    conn = sqlite3.connect("data/medicare.db")

    start = time.time()
    query = """
    WITH specialty_level AS (
        SELECT
            provider_type,
            npi,
            SUM(total_services) AS total_services,
            SUM(avg_medicare_payment * total_services) AS weighted_payment
        FROM medicare_payments
        WHERE provider_type IS NOT NULL
        GROUP BY provider_type, npi
    )
    SELECT
        provider_type,
        COUNT(DISTINCT npi) AS provider_count,
        SUM(total_services) AS total_services,
        ROUND(SUM(weighted_payment) / SUM(total_services), 2) AS cost_per_service
    FROM specialty_level
    GROUP BY provider_type
    ORDER BY cost_per_service DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv('outputs/result_csvs/payments_by_speciality.csv', index=False)
    total_time = time.time() - start
    print("Query 3: Payments by Speciality")
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    # Close connection
    conn.close()
    return df

# Query 4: Procedures with highest payment variation across provider types
def procedure_payment_variation():
    conn = sqlite3.connect("data/medicare.db")
    start = time.time()
    query = """
    WITH provider_level AS (
        SELECT
            npi,
            MAX(provider_type) AS provider_type,
            hcpcs_code,
            MAX(hcpcs_description) as hcpcs_description,
            SUM(total_services) AS total_services,
            AVG(avg_medicare_payment) AS avg_payment
        FROM medicare_payments
        WHERE provider_type IS NOT NULL
        GROUP BY npi, hcpcs_code
    ),
    hcpcs_summary AS (
        SELECT
            hcpcs_code,
            MAX(hcpcs_description) AS hcpcs_description,
            COUNT(DISTINCT provider_type) AS num_provider_type,
            SUM(total_services) AS total_services,
            AVG(avg_payment) AS mean_payment,
            MAX(avg_payment) - MIN(avg_payment) AS payment_variation
        FROM provider_level
        GROUP BY hcpcs_code
    )
    SELECT *
    FROM hcpcs_summary
    WHERE total_services > 1000
    ORDER BY payment_variation DESC
    LIMIT 20
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv('outputs/result_csvs/procedure_payment_variation.csv', index=False)
    total_time = time.time() - start
    print("Query 4: Payment Variation by Procedure")
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    # Close connection
    conn.close()
    return df

# Query 5: Medicare payments in states with major VA facilities
def medicare_va_states():
    conn = sqlite3.connect("data/medicare.db")
    start = time.time()

    query = """
    SELECT
        v.state,
        v.facility_name,
        COUNT(DISTINCT m.npi) as medicare_providers,
        SUM(m.total_services) as total_medicare_services,
        ROUND(SUM(m.avg_medicare_payment), 2) as avg_medicare_payment
    FROM va_facilities v
    LEFT JOIN medicare_payments m ON v.state = m.provider_state
    GROUP BY v.state, v.facility_name
    ORDER BY avg_medicare_payment DESC
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv('outputs/result_csvs/medicare_va_states.csv', index=False)
    total_time = time.time() - start
    print("Query 5: Medicare Payments in VA Facility States")
    print(f"Query time: {total_time:.2f} seconds")
    print("\n")

    # Close connection
    conn.close()
    return df




