import sqlite3

conn = sqlite3.connect('gas_booking.db')
cursor = conn.cursor()

# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
)
''')

# BOOKINGS TABLE (FIXED - now linked to user)
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    cylinder_type TEXT,
    amount TEXT,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()

print("Database Created Successfully with Relations")
