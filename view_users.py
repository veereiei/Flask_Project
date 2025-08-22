import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# ดูว่ามีตารางอะไรบ้าง
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# ดึงข้อมูลผู้ใช้
cursor.execute("SELECT * FROM user;")
rows = cursor.fetchall()

print("\nUsers:")
for row in rows:
    print(row)

conn.close()
