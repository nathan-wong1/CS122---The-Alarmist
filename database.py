import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_path="alarmist.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
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

    def add_alarm(self, title, alarm_date, alarm_time, description):
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._connect() as conn:
            conn.execute("""
                INSERT INTO Alarms (title, created_time, alarm_date, alarm_time, description, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (title, created_time, alarm_date, alarm_time, description, 1))

    def get_alarms(self):
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT id, title, alarm_date, alarm_time, description
                FROM Alarms
                WHERE is_active = 1
                ORDER BY alarm_date, alarm_time
            """)
            return cursor.fetchall()

    def delete_alarm(self, alarm_id):
        with self._connect() as conn:
            conn.execute("DELETE FROM Alarms WHERE id = ?", (alarm_id,))