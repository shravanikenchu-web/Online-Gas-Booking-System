from flask import Flask, render_template, request, redirect, session
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "gas_booking_secret_key"


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('01_index.html')


# ---------------- CUSTOMER LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        consumer_id = request.form['consumer_id']
        mobile = request.form['mobile']

        conn = sqlite3.connect('gas_booking.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE consumer_id=? AND mobile=?",
            (consumer_id, mobile)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['consumer_id'] = user[2]
            session['mobile'] = user[3]

            return redirect('/dashboard')

        return "Invalid Consumer ID or Mobile Number"

    return render_template('02_login.html')


# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():

    if 'consumer_id' not in session:
        return redirect('/login')

    return render_template('03_dashboard.html')


# ---------------- BOOKING ----------------
@app.route('/booking', methods=['GET', 'POST'])
def booking():

    if 'consumer_id' not in session:
        return redirect('/login')

    if request.method == 'POST':

        session['cylinder_type'] = request.form['cylinder_type']
        session['amount'] = request.form['amount']

        otp = str(random.randint(1000, 9999))
        session['otp'] = otp

        print("OTP =", otp)

        return redirect('/verify_otp')

    return render_template('04_booking.html')


# ---------------- OTP VERIFY ----------------
@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():

    if request.method == 'POST':

        entered_otp = request.form['otp']

        if entered_otp == session.get('otp'):

            conn = sqlite3.connect('gas_booking.db')
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO bookings
            (consumer_id,name,mobile,cylinder_type,amount,status)
            VALUES(?,?,?,?,?,?)
            """,
            (
                session['consumer_id'],
                session['name'],
                session['mobile'],
                session['cylinder_type'],
                session['amount'],
                "Booked"
            ))

            conn.commit()
            conn.close()

            return redirect('/payment')

        return "Invalid OTP"

    return render_template('05_verify_otp.html')


# ---------------- PAYMENT ----------------
@app.route('/payment', methods=['GET', 'POST'])
def payment():

    if 'consumer_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        return redirect('/history')

    return render_template('06_payment.html')


# ---------------- HISTORY ----------------
@app.route('/history')
def history():

    if 'consumer_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id,cylinder_type,amount,status
    FROM bookings
    WHERE consumer_id=?
    """, (session['consumer_id'],))

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


# ---------------- ADD CUSTOMER ----------------
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if 'admin' not in session:
        return redirect('/admin')

    if request.method == 'POST':

        name = request.form['name']
        consumer_id = request.form['consumer_id']
        mobile = request.form['mobile']

        conn = sqlite3.connect('gas_booking.db')
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users(name,consumer_id,mobile) VALUES(?,?,?)",
                (name, consumer_id, mobile)
            )

            conn.commit()

        except Exception as e:
    conn.close()
    print(e)   # logs error in Render logs
    return "Something went wrong"

        conn.close()

        return redirect('/view_users')

    return render_template('10_add_customer.html')


# ---------------- VIEW USERS ----------------
@app.route('/view_users')
def view_users():

    if 'admin' not in session:
        return redirect('/admin')

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    conn.close()

    return render_template('11_view_users.html', users=users)


# ---------------- VIEW BOOKINGS ----------------
@app.route('/view_bookings')
def view_bookings():

    if 'admin' not in session:
        return redirect('/admin')

    conn = sqlite3.connect('gas_booking.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    id,
    consumer_id,
    name,
    mobile,
    cylinder_type,
    amount,
    status
    FROM bookings
    """)

    bookings = cursor.fetchall()

    conn.close()

    return render_template(
        '12_view_bookings.html',
        bookings=bookings
    )


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
