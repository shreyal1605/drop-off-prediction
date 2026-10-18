import sqlite3
import pandas as pd
import numpy as np

# 1. This creates a local file named 'kaabil_pm_portfolio.db' on your computer
conn = sqlite3.connect("project1.db")
cursor = conn.cursor()

# 2. Create the tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    signup_date TEXT,
    platform TEXT,
    app_version TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS funnel_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    stage_name TEXT,
    event_timestamp TEXT
)
""")

# 3. Insert realistic rural onboarding data
np.random.seed(42)
n_users = 500
user_ids = [f"USR_{i:04d}" for i in range(1, n_users + 1)]
platforms = np.random.choice(["Android", "iOS"], size=n_users, p=[0.75, 0.25])
app_versions = np.random.choice(["v2.4.1", "v2.3.0"], size=n_users, p=[0.6, 0.4])

users_data = []
funnel_data = []
stages = ["1_signup", "2_phone_verified", "3_kyc_submitted", "4_loan_applied"]

for i, uid in enumerate(user_ids):
    signup_date = f"2026-03-{np.random.randint(1, 28):02d} 10:00:00"
    users_data.append((uid, signup_date, platforms[i], app_versions[i]))
    
    # Simulate drop-offs across stages
    reached = np.random.choice([1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.4])
    for s_idx in range(reached):
        funnel_data.append((uid, stages[s_idx], signup_date))

cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?)", users_data)
cursor.executemany("INSERT INTO funnel_events (user_id, stage_name, event_timestamp) VALUES (?, ?, ?)", funnel_data)
conn.commit()

# Add region column if not exists
try:
    cursor.execute("ALTER TABLE users ADD COLUMN region TEXT;")
    conn.commit()
except sqlite3.OperationalError:
    pass # Column already exists

# Assign random regions to existing users
regions = ["Rajasthan", "Uttar Pradesh", "Bihar", "Madhya Pradesh"]
cursor.execute("SELECT user_id FROM users")
users = cursor.fetchall()

np.random.seed(42)
for u in users:
    reg = np.random.choice(regions, p=[0.4, 0.3, 0.2, 0.1])
    cursor.execute("UPDATE users SET region = ? WHERE user_id = ?", (reg, u[0]))
conn.commit()

print("Database created and seeded with 500 users!")
conn.close()