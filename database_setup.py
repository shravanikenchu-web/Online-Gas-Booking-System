import sqlite3

conn = sqlite3.connect('gas_booking.db')
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    consumer_id TEXT UNIQUE NOT NULL,
    mobile TEXT NOT NULL
)
""")

# BOOKINGS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consumer_id TEXT,
    cylinder_type TEXT,
    amount TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")
