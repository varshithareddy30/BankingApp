from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize account table
def init_db():
    if not os.path.exists("database/bank.db"):
        os.makedirs("database", exist_ok=True)
        conn = sqlite3.connect("database/bank.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                balance INTEGER NOT NULL
            );
        """)
        cursor.execute("INSERT INTO account (balance) VALUES (0);")
        conn.commit()
        conn.close()

# Initialize users table
def init_users():
    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            balance INTEGER NOT NULL
        );
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, email, balance) VALUES (?, ?, ?)", 
                       ("Tondapu Varshitha Reddy", "varshitha@gmail.com", 5000))
    conn.commit()
    conn.close()

# Welcome Page
@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            return redirect(url_for('dashboard'))
        else:
            error = "Please enter both username and password."
    return render_template('login.html', error=error)

# Get account balance
def get_balance():
    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM account WHERE id = 1")
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

# Update balance
def update_balance(amount, operation):
    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()
    current_balance = get_balance()

    if operation == "deposit":
        new_balance = current_balance + amount
    elif operation == "withdraw":
        if amount > current_balance:
            conn.close()
            return False
        new_balance = current_balance - amount

    cursor.execute("UPDATE account SET balance = ? WHERE id = 1", (new_balance,))
    conn.commit()
    conn.close()
    return True

# Dashboard
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', users=users)

# Deposit
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    message = ''
    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])
            if amount <= 0:
                message = "Enter a valid amount!"
            else:
                update_balance(amount, "deposit")
                message = f"₹{amount} deposited successfully!"
        except:
            message = "Invalid input. Please enter a number."
    return render_template('deposit.html', message=message)

# Withdraw
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    message = ''
    if request.method == 'POST':
        try:
            amount = int(request.form['amount'])
            if amount <= 0:
                message = "Enter a valid amount!"
            else:
                success = update_balance(amount, "withdraw")
                if success:
                    message = f"₹{amount} withdrawn successfully!"
                else:
                    message = "Insufficient balance."
        except:
            message = "Invalid input. Please enter a number."
    return render_template('withdraw.html', message=message)

# Check Balance
@app.route('/balance')
def balance():
    current_balance = get_balance()
    return render_template('balance.html', balance=current_balance)

# Transfer Money
@app.route('/transfer', methods=['POST'])
def transfer():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = int(request.form['amount'])

    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM users WHERE name=?", (sender,))
    sender_data = cursor.fetchone()
    if not sender_data or sender_data[0] < amount:
        conn.close()
        return "Transfer failed: insufficient balance or sender not found."

    cursor.execute("SELECT balance FROM users WHERE name=?", (receiver,))
    receiver_data = cursor.fetchone()
    if not receiver_data:
        conn.close()
        return "Transfer failed: receiver not found."

    cursor.execute("UPDATE users SET balance = balance - ? WHERE name = ?", (amount, sender))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE name = ?", (amount, receiver))

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount INTEGER,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)",
                   (sender, receiver, amount))

    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

# View History
@app.route('/history')
def history():
    conn = sqlite3.connect("database/bank.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY time DESC")
    transactions = cursor.fetchall()
    conn.close()
    return render_template("history.html", transactions=transactions)

# Start app
if __name__ == '__main__':
    init_db()
    init_users()
    app.run(debug=True)