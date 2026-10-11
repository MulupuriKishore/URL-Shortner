import sqlite3

conn = sqlite3.connect("instance/urls.db")

cursor = conn.cursor()

cursor.execute("""
    ALTER TABLE url
    ADD COLUMN click_counter INTEGER NOT NULL DEFAULT 0
""")

conn.commit()
conn.close()

print("Column added successfully")