import sqlite3


def create_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT,
                      last_name TEXT,
                      username TEXT,
                      chat_id BIGINT)''')

    conn.commit()

    cursor.close()
    conn.close()


def insert_query(last_name, first_name, username, chat_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO users (last_name, first_name, username, chat_id) "
                   "VALUES (?, ?, ?, ?)", (last_name, first_name, username, chat_id))

    conn.commit()

    cursor.close()
    conn.close()


def get_all_users():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return users


def get_user_by_chat_id(chat_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE chat_id=%s", (chat_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
