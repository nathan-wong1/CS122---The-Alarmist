import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect("alarmist.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Alarms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created_time TEXT NOT NULL,
        alarm_date TEXT NOT NULL,
        alarm_time TEXT NOT NULL,
        description TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)
    conn.commit()
    conn.close()

def add_alarm(title, alarm_date, alarm_time, description):
    conn = connect_db()
    cursor = conn.cursor()
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO Alarms (title, created_time, alarm_date, alarm_time, description, is_active)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (title, created_time, alarm_date, alarm_time, description, 1))

    conn.commit()
    conn.close()

def view_alarms():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Alarms")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No alarms found.")

def delete_alarm(alarm_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Alarms WHERE id = ?", (alarm_id,))
    conn.commit()
    conn.close()

create_table()
add_alarm("Morning Alarm", "2026-04-15", "07:30 AM", "Wake up for class")
view_alarms()