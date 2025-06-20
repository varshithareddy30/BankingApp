🏦 MyBank - Flask-Based Mini Banking Application

MyBank is a mini web application built using Flask and SQLite that simulates basic banking operations. It features a clean user interface and performs operations like deposits, withdrawals, transfers, and tracks transaction history.

🔧 Features

🧍 View all bank users with their balances

➕ Deposit and ➖ Withdraw money

🔄 Transfer money from one user to another

📜 View full transaction history with date and time

🔐 Login page before accessing the dashboard

🎨 Beautiful UI with images and styling for better experience


🛠 Technologies Used

Python (Flask)

SQLite (Database)

HTML/CSS

JavaScript (Voice input optional)

Bootstrap & Font Awesome (for styling/icons)


📁 Project Structure

BankingApp/
│
├── app.py                  # Main Flask backend
├── database/
│   └── bank.db             # SQLite database
├── templates/
│   ├── welcome.html
│   ├── login.html
│   ├── dashboard.html
│   ├── deposit.html
│   ├── withdraw.html
│   ├── balance.html
│   └── history.html
├── static/
│   └── style.css           # All CSS styles
│   └── bank_dashboard.png  # Dashboard background

🚀 How to Run

1. Make sure Python and Flask are installed


2. Run: python app.py


3. Open your browser and go to http://localhost:5000/welcome
4.
