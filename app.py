from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create tables automatically
def create_tables():
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

        conn = sqlite3.connect('gas_booking.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('02_register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('gas_booking.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect('/dashboard')
        else:
            return "Invalid Email or Password!"

    return render_template('03_login.html')


@app.route('/dashboard')
def dashboard():
    return render_template('04_dashboard.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if request.method == 'POST':

        cylinder_type = request.form['cylinder_type']
        amount = request.form['amount']

        conn = sqlite3.connect('gas_booking.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO bookings(cylinder_type, amount, status) VALUES(?,?,?)",
            (cylinder_type, amount, 'Booked')
        )

        conn.commit()
        conn.close()

        return "Booking Successful!"

    return render_template('05_booking.html')


@app.route('/history')
def history():

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        '07_history.html',
        bookings=bookings
    )


@app.route('/logout')
def logout():
    return redirect('/')


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


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('09_admin_dashboard.html')


@app.route('/view_bookings')
def view_bookings():

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        '10_view_bookings.html',
        bookings=bookings
    )


@app.route('/view_users')
def view_users():

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return render_template(
        '11_view_users.html',
        users=users
    )
@app.route('/payment')
def payment():
    return render_template('06_payment.html')

if __name__ == '__main__':
    app.run(debug=True)
