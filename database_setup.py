import sqlite3

# Create Database
conn = sqlite3.connect('gas_booking.db')
cursor = conn.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create Bookings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cylinder_type TEXT NOT NULL,
    amount TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# Save Changes
conn.commit()

# Close Connection
conn.close()

print("Database Created Successfully")
