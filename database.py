import sqlite3

DB_PATH = 'users.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT,
            age INTEGER,
            phone TEXT,
            locality TEXT,
            language TEXT
        )''')
        conn.commit()
    
def get_user_by_email(email):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        return dict(user) if user else None    
    
def get_user_by_id(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        return dict(user) if user else None

def add_user(username, email, password, age, phone, locality, language):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, email, password, age, phone, locality, language)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (username, email, password, age, phone, locality, language))
        conn.commit()
        return c.lastrowid

def update_user(user_id, username, email, age, phone, locality, language):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE users
            SET username=?, email=?, age=?, phone=?, locality=?, language=?
            WHERE id=?
        ''', (username, email, age, phone, locality, language, user_id))
        conn.commit()

def delete_user(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()