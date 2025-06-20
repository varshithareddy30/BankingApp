import sqlite3

conn = sqlite3.connect("database/bank.db")
cursor = conn.cursor()

# Add another user
users=[("Nali Nandini Yadav","pandi@gmail.com",4000),
       ("Ambati Sannidha Raj","sanni@gmail.com",4000)]
cursor.executemany("INSERT INTO users (name, email, balance) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()

print("✅ New user added successfully!")