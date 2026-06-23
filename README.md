Online Gas Booking System

Project Description

The Online Gas Booking System is a web-based application developed using Flask and SQLite. In this system, the Admin creates customer accounts by providing a Consumer ID and Mobile Number. Customers can log in using their Consumer ID and registered Mobile Number, verify OTP, and book LPG cylinders online. The system also allows customers to view booking history, while the Admin can manage customers and monitor all bookings.

Technologies Used

- Python
- Flask
- SQLite3
- HTML5
- CSS3
- Bootstrap 5
- Gunicorn
- Render Deployment
- GitHub

Features

Customer Module

- Customer Login using Consumer ID
- Mobile Number Verification
- OTP Verification
- Customer Dashboard
- LPG Cylinder Booking
- Booking History
- Logout

Admin Module

- Admin Login
- Admin Dashboard
- Add Customer
- View Customers
- View All Bookings

Database Tables

Users Table

- ID
- Customer Name
- Consumer ID
- Mobile Number

Bookings Table

- Booking ID
- Consumer ID
- Customer Name
- Mobile Number
- Cylinder Type
- Amount
- Status

Project Structure

Online-Gas-Booking-System/

├── app.py

├── database_setup.py

├── requirements.txt

├── Procfile

├── README.md

├── static/

└── templates/

├── 01_index.html

├── 02_login.html

├── 03_dashboard.html

├── 04_booking.html

├── 05_verify_otp.html

├── 06_payment.html

├── 07_history.html

├── 08_admin_login.html

├── 09_admin_dashboard.html

├── 10_add_customer.html

├── 11_view_users.html

└── 12_view_bookings.html

Installation

1. Clone the repository

2. Install dependencies

pip install -r requirements.txt

3. Run the application

python app.py

4. Open browser

http://127.0.0.1:5000

Deployment

The project is deployed on Render using Gunicorn.

Future Enhancements

- Real SMS OTP Integration
- Online Payment Gateway
- Cylinder Delivery Tracking
- Customer Notifications
- PostgreSQL Database Integration

Developed By

Shravani Kenchu

MCA Final Year Project
