import sqlite3

def show_all_users():
    conn = sqlite3.connect("teentreasure_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    print("Registered Users:")
    for user in users:
        print(f"Username: {user[0]}, Password (Hashed): {user[1]}")

show_all_users()
