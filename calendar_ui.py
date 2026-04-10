import sys
import sqlite3
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QCalendarWidget
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QBrush

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "alarmist.db")

def connect_db():
    return sqlite3.connect(DB_NAME)


def get_events_by_date(selected_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, alarm_time, description
        FROM Alarms
        WHERE alarm_date = ?
        ORDER BY alarm_time
    """, (selected_date,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_event_dates():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT alarm_date FROM Alarms")
    rows = cursor.fetchall()
    conn.close()

    return [row[0] for row in rows]


class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Alarmist - Calendar UI")
        self.setGeometry(200, 200, 600, 500)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Client Calendar and Events")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.show_events_for_date)
        self.layout.addWidget(self.calendar)

        self.events_label = QLabel("Events for selected date:")
        self.events_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.layout.addWidget(self.events_label)

        self.events_list = QListWidget()
        self.layout.addWidget(self.events_list)

        self.setLayout(self.layout)

        self.highlight_event_dates()

        today = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.show_events_for_date(QDate.fromString(today, "yyyy-MM-dd"))

    def highlight_event_dates(self):
        event_dates = get_all_event_dates()

        format_with_event = QTextCharFormat()
        format_with_event.setBackground(QBrush())  
        format_with_event.setFontUnderline(True)

        for date_str in event_dates:
            qdate = QDate.fromString(date_str, "yyyy-MM-dd")
            if qdate.isValid():
                self.calendar.setDateTextFormat(qdate, format_with_event)

    def show_events_for_date(self, date):
        selected_date = date.toString("yyyy-MM-dd")
        events = get_events_by_date(selected_date)

        self.events_label.setText(f"Events for {selected_date}:")
        self.events_list.clear()

        if events:
            for title, alarm_time, description in events:
                text = f"{alarm_time} - {title}"
                if description:
                    text += f" | {description}"
                self.events_list.addItem(QListWidgetItem(text))
        else:
            self.events_list.addItem("No events for this date.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarApp()
    window.show()
    sys.exit(app.exec_())