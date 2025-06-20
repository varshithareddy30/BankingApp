import sqlite3

conn = sqlite3.connect("database/bank.db")
cursor = conn.cursor()

# Update name and balance where the email matches
cursor.execute("""
    UPDATE users
    SET name = ?, balance = ?
    WHERE email = ?
""", ("Tondapu Varshitha Reddy", 10000, "varshitha@example.com"))  # <-- change balance if needed

conn.commit()
conn.close()

print("✅ User updated successfully!")