# Flask User Management System

A Flask blueprint application that allows users to register with their information and provides an admin panel to view all registered users.

## Features

- User registration with name, UID (8+ digits), and email
- UID validation (must be numeric with minimum 8 digits)
- SQLite database storage
- Admin login system with math captcha security
- Admin dashboard with user management (edit/delete users)
- CSV export functionality for user data
- Bootstrap-styled responsive UI
- Blueprint architecture for modular code

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

3. Open your browser and go to `http://localhost:5000`

## Usage

### User Registration
- Navigate to the registration page
- Fill in the required fields: Name, UID (must be at least 8 digits), and Email
- Submit the form to register

### Admin Access
- Go to `/admin/login`
- Use the following credentials:
  - Username: `raymond.tsang`
  - Password: `Academy!234`
- Solve the math captcha (simple addition)
- View all registered users in the admin dashboard
- Edit user information by clicking the edit button
- Delete users with confirmation modal
- Export all user data to CSV format

## Project Structure

```
├── app.py              # Main application factory
├── run.py              # Application runner
├── models.py           # Database models
├── requirements.txt    # Python dependencies
├── blueprints/
│   ├── __init__.py
│   ├── main.py         # Main routes (home, registration)
│   └── admin.py        # Admin routes (login, dashboard)
└── templates/
    ├── base.html       # Base template with Bootstrap
    ├── index.html      # Home page
    ├── register.html   # User registration form
    └── admin/
        ├── login.html  # Admin login form
        └── dashboard.html # Admin dashboard with user table
```

## Technologies Used

- Flask (Python web framework)
- Flask-SQLAlchemy (Database ORM)
- SQLite (Database)
- Bootstrap 5 (CSS framework)
- Jinja2 (Template engine)