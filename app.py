from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "gas_booking_secret_key"

# ✅ FIXED DATABASE PATH (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gas_booking.db")


# Create tables automatically
def create_tables():
    conn = sqlite3.connect('gas_booking.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # USERS TABLE (FIXED: email UNIQUE + proper structure)
    # USERS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
@@ -19,7 +25,7 @@ def create_tables():
    )
    ''')

    # BOOKINGS TABLE (FIXED: linked to user_id)
    # BOOKINGS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
@@ -42,7 +48,7 @@ def home():
    return render_template('01_index.html')


# Register (FIXED: duplicate prevention)
# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

@@ -52,10 +58,10 @@ def register():
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('gas_booking.db')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # CHECK DUPLICATE USER
        # check duplicate
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing = cursor.fetchone()

@@ -86,7 +92,7 @@ def login():
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('gas_booking.db')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
@@ -116,7 +122,7 @@ def dashboard():
    return render_template('04_dashboard.html')


# Booking (FIXED: store user_email)
# Booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():

@@ -129,7 +135,7 @@ def booking():
        amount = request.form['amount']
        user_email = session['user']

        conn = sqlite3.connect('gas_booking.db')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
@@ -155,7 +161,7 @@ def payment(booking_id):
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('gas_booking.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
@@ -169,14 +175,14 @@ def payment(booking_id):
    return render_template('06_payment.html')


# HISTORY (FIXED: show only logged-in user data)
# History (FIXED)
@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('gas_booking.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
@@ -221,11 +227,11 @@ def admin_dashboard():
    return render_template('09_admin_dashboard.html')


# View bookings (ADMIN)
# View bookings
@app.route('/view_bookings')
def view_bookings():

    conn = sqlite3.connect('gas_booking.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
@@ -236,11 +242,11 @@ def view_bookings():
    return render_template('10_view_bookings.html', bookings=bookings)


# View users (ADMIN)
# View users
@app.route('/view_users')
def view_users():

    conn = sqlite3.connect('gas_booking.db')
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    
users = cursor.fetchall()

    conn.close()

    return render_template('11_view_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
