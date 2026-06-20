import sqlite3

conn = sqlite3.connect('gas_booking.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cylinder_type TEXT,
    amount TEXT,
    status TEXT
)
''')
conn.commit()
conn.close()

print("Database Created Successfully")
