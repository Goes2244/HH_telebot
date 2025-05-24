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
    chat_id INTEGER,  
    candidate TEXT,
    datetime TEXT,
    type TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS manual_resumes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    position TEXT,
    city TEXT,
    experience TEXT,
    resume_link TEXT,
    added_by INTEGER
)
''')

conn.commit()

# --- Функции для работы с заметками ---
def add_note(candidate, note):
    cursor.execute("INSERT INTO notes (candidate, note) VALUES (?, ?)", (candidate, note))
    conn.commit()

def get_notes(candidate):
    cursor.execute("SELECT id, note FROM notes WHERE candidate = ?", (candidate,))
    return cursor.fetchall()

def delete_note(note_id):
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()

# --- Функции для работы с напоминаниями ---
def add_reminder(chat_id, candidate, dt, r_type):
    cursor.execute(
        "INSERT INTO reminders (chat_id, candidate, datetime, type) VALUES (?, ?, ?, ?)",
        (chat_id, candidate, dt, r_type)
    )
    conn.commit()
    return cursor.lastrowid  

def get_reminders():  
    cursor.execute("SELECT id, chat_id, candidate, datetime, type FROM reminders")
    return cursor.fetchall()

def get_reminders_by_user_and_time(user_id, start_time, end_time):
    cursor.execute(
        "SELECT * FROM reminders WHERE chat_id = ? AND datetime BETWEEN ? AND ?",
        (user_id, start_time.isoformat(), end_time.isoformat())
    )
    return cursor.fetchall()

def delete_reminder(reminder_id):  
    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))
    conn.commit()

# --- Функции для работы с резюме ---
def add_manual_resume(full_name, position, city, experience, resume_link, added_by):
    cursor.execute(
        "INSERT INTO manual_resumes (full_name, position, city, experience, resume_link, added_by) VALUES (?, ?, ?, ?, ?, ?)",
        (full_name, position, city, experience, resume_link, added_by)
    )
    conn.commit()