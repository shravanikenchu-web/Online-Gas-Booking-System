            from flask import Flask, render_template, request, redirect, session, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "gas_booking_secret_key"

DATABASE_URL = "postgresql://online_gas_booking_system_user:SovsbFtIkVSI1Iv0wpxgcE1ZziROpHYd@dpg-d8qi2da8qa3s73ca415g-a/online_gas_booking_system"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id SERIAL PRIMARY KEY,
        user_email TEXT,
        cylinder_type TEXT,
        amount TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

create_tables()

@app.route('/')
def home():
    return render_template('01_index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            flash("User already exists! Please login.")
            return redirect('/login')

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        flash("Registration Successful!")
        return redirect('/login')

    return render_template('02_register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
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

        flash("Invalid credentials!")
        return redirect('/login')

    return render_template('03_login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('04_dashboard.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        cylinder_type = request.form['cylinder_type']
        amount = request.form['amount']
        user_email = session['user']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bookings(user_email, cylinder_type, amount, status)
            VALUES(%s,%s,%s,%s)
            RETURNING id
        """, (user_email, cylinder_type, amount, "Booked"))

        booking_id = cursor.fetchone()[0]

        conn.commit()
        conn.close()

        return redirect(f'/payment/{booking_id}')

    return render_template('05_booking.html')

@app.route('/payment/<int:booking_id>')
def payment(booking_id):
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE bookings SET status=%s WHERE id=%s",
        ("Paid", booking_id)
    )

    conn.commit()
    conn.close()

    return render_template('06_payment.html')

@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, cylinder_type, amount, status FROM bookings WHERE user_email=%s",
        (session['user'],)
    )

    bookings = cursor.fetchall()
    conn.close()

    return render_template('07_history.html', bookings=bookings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return redirect('/admin_dashboard')

        return "Invalid Admin Credentials"

    return render_template('08_admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('09_admin_dashboard.html')

@app.route('/view_bookings')
def view_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
    bookings = cursor.fetchall()

    conn.close()

    return render_template('10_view_bookings.html', bookings=bookings)

@app.route('/view_users')
def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()

    conn.close()

    return render_template('11_view_users.html', users=users)

if __name__ == '__main__':
    app.run()
