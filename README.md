# Online Gas Booking System

## Project Description

The Online Gas Booking System is a web-based application developed using Flask and SQLite. It allows users to register, log in, book gas cylinders online, view booking history, and manage bookings through an admin dashboard.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- Gunicorn
- Render Deployment

## Features

### User Module

- User Registration
- User Login
- User Dashboard
- Gas Cylinder Booking
- Booking History
- Logout

### Admin Module

- Admin Login
- Admin Dashboard
- View All Users
- View All Bookings

## Database Tables

### Users Table

- User ID
- Name
- Email
- Password

### Bookings Table

- Booking ID
- Cylinder Type
- Amount
- Status

## Project Structure

Online-Gas-Booking-System/

├── app.py

├── database_setup.py

├── requirements.txt

├── Procfile

├── README.md

├── static/

│ └── style.css

└── templates/

├── 01_index.html

├── 02_register.html

├── 03_login.html

├── 04_dashboard.html

├── 05_booking.html

├── 06_payment.html

├── 07_history.html

├── 08_admin_login.html

├── 09_admin_dashboard.html

├── 10_view_bookings.html

└── 11_view_users.html

## Installation

1. Clone the repository

2. Install dependencies

pip install -r requirements.txt

3. Run the application

python app.py

4. Open browser

http://127.0.0.1:5000

## Deployment

The project is deployed on Render using Gunicorn.

## Future Enhancements

- Online Payment Gateway
- Email Notifications
- Cylinder Delivery Tracking
- User Profile Management
- PostgreSQL Database Integration

## Developed By

Shravani Kenchu

MCA Final Year Project
