import sqlite3

def get_connection():
    conn = sqlite3.connect('users.db')
    return conn

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(username, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )
    conn.commit()
    conn.close()
    return {"status": "created"}

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    return results