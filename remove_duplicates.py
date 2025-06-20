import sqlite3

conn = sqlite3.connect("database/bank.db")
cursor = conn.cursor()

# Delete duplicate users keeping only one per email
cursor.execute("""
    DELETE FROM users
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM users
        GROUP BY email
    );
""")

conn.commit()
conn.close()

print("✅ Duplicates removed successfully!")