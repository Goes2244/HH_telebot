import sqlite3

conn = sqlite3.connect("bot_data.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate TEXT,
    note TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate TEXT,
    datetime TEXT,
    type TEXT
)
''')

conn.commit()

def add_note(candidate, note):
    cursor.execute("INSERT INTO notes (candidate, note) VALUES (?, ?)", (candidate, note))
    conn.commit()

def get_notes(candidate):
    cursor.execute("SELECT note FROM notes WHERE candidate = ?", (candidate,))
    return [row[0] for row in cursor.fetchall()]

def add_reminder(candidate, dt, r_type):
    cursor.execute("INSERT INTO reminders (candidate, datetime, type) VALUES (?, ?, ?)", (candidate, dt, r_type))
    conn.commit()

def get_reminders():
    cursor.execute("SELECT candidate, datetime, type FROM reminders")
    return cursor.fetchall()
