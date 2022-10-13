import sqlite3

conn = sqlite3.connect("../TestDb")

cursor = conn.cursor()
cursor.execute("Select * From Product")
rows = cursor.fetchall()

print(rows)
