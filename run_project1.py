import sqlite3
import pandas as pd

# 1. Connect to a local SQLite database file
conn = sqlite3.connect("project1.db")

query = """
SELECT 
    stage_name,
    COUNT(DISTINCT user_id) AS user_count,
    ROUND(COUNT(DISTINCT user_id) * 100.0 / (SELECT COUNT(DISTINCT user_id) FROM users), 2) AS conversion_pct
FROM funnel_events
GROUP BY stage_name
ORDER BY stage_name;
"""
df = pd.read_sql(query, conn)
print("\n--- ONBOARDING FUNNEL RESULTS ---")
print(df)

query2 = """
SELECT 
    u.platform,
    COUNT(DISTINCT u.user_id) AS total_users,
    SUM(CASE WHEN f.stage_name = '3_kyc_submitted' THEN 1 ELSE 0 END) AS kyc_completed,
    ROUND(SUM(CASE WHEN f.stage_name = '3_kyc_submitted' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT u.user_id), 2) as kyc_conversion_rate
FROM users u
LEFT JOIN funnel_events f ON u.user_id = f.user_id
GROUP BY u.platform;
"""
df_sliced = pd.read_sql(query2, conn)
print("\n--- FUNNEL SLICED BY PLATFORM ---")
print(df_sliced)

query3 = """
SELECT 
    u.app_version,
    COUNT(DISTINCT u.user_id) AS total_users,
    SUM(CASE WHEN f.stage_name = '3_kyc_submitted' THEN 1 ELSE 0 END) AS kyc_completed,
    ROUND(SUM(CASE WHEN f.stage_name = '3_kyc_submitted' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT u.user_id), 2) as kyc_conversion_rate
FROM users u
LEFT JOIN funnel_events f ON u.user_id = f.user_id
GROUP BY u.app_version;
"""
df_version = pd.read_sql(query3, conn)
print("\n--- SLICED BY APP VERSION ---")
print(df_version)

query4 = """
WITH user_kyc AS (
    SELECT DISTINCT user_id 
    FROM funnel_events 
    WHERE stage_name = '3_kyc_submitted'
)
SELECT 
    u.region,
    COUNT(DISTINCT u.user_id) AS total_users,
    COUNT(DISTINCT uk.user_id) AS kyc_completed,
    ROUND(COUNT(DISTINCT uk.user_id) * 100.0 / COUNT(DISTINCT u.user_id), 2) AS kyc_conversion_rate
FROM users u
LEFT JOIN user_kyc uk ON u.user_id = uk.user_id
GROUP BY u.region
ORDER BY kyc_conversion_rate ASC;
"""

df_fixed = pd.read_sql(query4, conn)
print("\n--- FIXED REGIONAL CONVERSION ---")
print(df_fixed)

print("Database and tables created successfully!")
conn.close()