from flask import Flask, render_template, request, redirect, session, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "gas_booking_secret_key"

DATABASE_URL = "postgresql://online_gas_booking_system_user:SovsbFtIkVSI1Iv0wpxgcE1ZziROpHYd@dpg-d8qi2da8qa3s73ca415g-a/online_gas_booking_system"

# ✅ FIXED DATABASE PATH (IMPORTANT)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "gas_booking.db")


# Create tables automatically
def create_tables():
    conn = sqlite3.connect(DB_PATH)
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

    # BOOKINGS TABLE
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        cylinder_type TEXT,
        amount TEXT,
        status TEXT
    )
    ''')

    conn.commit()
    conn.close()

create_tables()


# Home
@app.route('/')
def home():
    return render_template('01_index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # check duplicate
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        existing = cursor.fetchone()

        if existing:
            flash("User already exists! Please login.")
            return redirect('/login')

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful! Please login.")
        return redirect('/login')

    return render_template('02_register.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = email
            flash("Login Successful!")
            return redirect('/dashboard')
        else:
            flash("Invalid credentials!")
            return redirect('/login')

    return render_template('03_login.html')


# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('04_dashboard.html')


# Booking
@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':

        cylinder_type = request.form['cylinder_type']
        amount = request.form['amount']
        user_email = session['user']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings(user_email, cylinder_type, amount, status) VALUES(?,?,?,?)",
            (user_email, cylinder_type, amount, 'Booked')
        )

        booking_id = cursor.lastrowid

        conn.commit()
        conn.close()

        flash("Booking Successful!")
        return redirect(f'/payment/{booking_id}')

    return render_template('05_booking.html')


# Payment
@app.route('/payment/<int:booking_id>')
def payment(booking_id):

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bookings SET status=? WHERE id=?",
        ("Paid", booking_id)
    )

    conn.commit()
    conn.close()

    return render_template('06_payment.html')


# History (FIXED)
@app.route('/history')
def history():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, cylinder_type, amount, status FROM bookings WHERE user_email=?",
        (session['user'],)
    )

    bookings = cursor.fetchall()
    conn.close()

    return render_template('07_history.html', bookings=bookings)


# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully!")
    return redirect('/')


# Admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return redirect('/admin_dashboard')
        else:
            return "Invalid Admin Credentials"

    return render_template('08_admin_login.html')


# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('09_admin_dashboard.html')


# View bookings
@app.route('/view_bookings')
def view_bookings():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template('10_view_bookings.html', bookings=bookings)


# View users
@app.route('/view_users')
def view_users():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('11_view_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
