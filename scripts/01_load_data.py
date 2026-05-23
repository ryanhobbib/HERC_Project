import sqlite3
import pandas as pd
import os

# Create database
conn = sqlite3.connect("data/medicare.db")
cursor = conn.cursor()

# Clear old data if it exists already
cursor.execute("DROP TABLE IF EXISTS medicare_payments")
conn.commit()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicare_payments (
    npi TEXT,
    provider_type TEXT,
    provider_state TEXT,
    hcpcs_code TEXT,
    hcpcs_description TEXT,
    total_services INTEGER,
    avg_medicare_payment REAL
)               
""")
conn.commit()

# Mapping to change original column names
column_map = {
    'Rndrng_NPI': 'npi',
    'Rndrng_Prvdr_Ent_Cd': 'provider_type',
    'Rndrng_Prvdr_State_Abrvtn': 'provider_state',
    'HCPCS_Cd': 'hcpcs_code',
    'HCPCS_Desc': 'hcpcs_description',
    'Tot_Srvcs': 'total_services',
    'Avg_Mdcr_Pymt_Amt': 'avg_medicare_payment'
}

# Import data in 100000 row chunks to save memory
for chunk in pd.read_csv("data/medicare.csv", chunksize=100000, low_memory=False):
    # Rename columns
    chunk = chunk.rename(columns=column_map)

    # Keep only necessary columns
    chunk = chunk[list(column_map.values())]

    chunk.to_sql('medicare_payments', conn, if_exists='append', index=False)

# Create indexes for faster querying
cursor.execute("CREATE INDEX idx_hcpcs ON medicare_payments(hcpcs_code)")
cursor.execute("CREATE INDEX idx_state ON medicare_payments(provider_state)")
cursor.execute("CREATE INDEX idx_type ON medicare_payments(provider_type)")
conn.commit()

# Check to make sure everything loaded correctly
cursor.execute("SELECT COUNT(*) FROM medicare_payments")
row_count = cursor.fetchone()[0]
print(f"Number of rows: {row_count}")

# Close database
conn.close()