from flask import Flask, render_template, request, redirect, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = "gas_booking_secret_key"

# ---------------- DATABASE CONNECTION ----------------
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# ---------------- CREATE TABLES ----------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id SERIAL PRIMARY KEY,
        email TEXT NOT NULL,
        cylinder_type TEXT NOT NULL,
        amount TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

create_tables()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('01_index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
                (name, email, password)
            )
            conn.commit()
        except:
            conn.close()
            return "Email already registered!"

        conn.close()
        return redirect('/login')

    return render_template('02_register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect('/dashboard')

        return "Invalid Email or Password!"

    return render_template('03_login.html')

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template('04_dashboard.html')

# ---------------- BOOKING ----------------
@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        cylinder_type = request.form['cylinder_type']
        amount = request.form['amount']
        email = session['user']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings(email,cylinder_type,amount,status) VALUES(%s,%s,%s,%s)",
            (email, cylinder_type, amount, "Booked")
        )

        conn.commit()
        conn.close()

        return redirect('/payment')

    return render_template('05_booking.html')

# ---------------- PAYMENT ----------------
@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        return redirect('/history')

    return render_template('06_payment.html')

# ---------------- HISTORY ----------------
@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    email = session['user']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE email=%s",
        (email,)
    )

    bookings = cursor.fetchall()
    conn.close()

    return render_template('07_history.html', bookings=bookings)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- ADMIN LOGIN ----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            session['admin'] = True
            return redirect('/admin_dashboard')

        return "Invalid Admin Credentials"

    return render_template('08_admin_login.html')

# ---------------- ADMIN DASHBOARD ----------------
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect('/admin')

    return render_template('09_admin_dashboard.html')

# ---------------- VIEW BOOKINGS ----------------
@app.route('/view_bookings')
def view_bookings():
    if 'admin' not in session:
        return redirect('/admin')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template('10_view_bookings.html', bookings=bookings)

# ---------------- VIEW USERS ----------------
@app.route('/view_users')
def view_users():
    if 'admin' not in session:
        return redirect('/admin')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template('11_view_users.html', users=users)

# ---------------- RUN ----------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
