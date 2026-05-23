import sqlite3
import pandas as pd
import os

# Create database
conn = sqlite3.connect("data/medicare.db")
cursor = conn.cursor()

# Load data
df = pd.read_csv("data/medicare.csv")

# Change column names
column_map = {
    'Rndrng_NPI': 'npi',
    'Rndrng_Prvdr_Ent_Cd': 'provider_type',
    'Rndrng_Prvdr_State_Abrvtn': 'provider_state',
    'HCPCS_Cd': 'hcpcs_code',
    'HCPCS_Desc': 'hcpcs_description',
    'Tot_Srvcs': 'total_services',
    'Avg_Mdcr_Pymt_Amt': 'avg_medicare_payment'
}
df = df.rename(columns=column_map)

# Import dataframe to database
df.to_sql('medicare_payments', conn, if_exists='replace', index=False)

# Create indexes for faster querying
cursor.execute("CREATE INDEX idx_hcpcs ON medicare_payments(hcpcs_code)")
cursor.execute("CREATE INDEX idx_state ON medicare_payments(provider_state)")
cursor.execute("CREATE INDEX idx_type ON medicare_payments(provider_type)")

# Check to make sure everything loaded correctly
cursor.execute("SELECT COUNT(*) FROM medicare_payments")
row_count = cursor.fetchone()[0]
print(f"Number of rows: {row_count}")

# Close database
conn.commit()
conn.close()