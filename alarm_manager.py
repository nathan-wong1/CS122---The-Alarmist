class AlarmManager:
    def __init__(self, window, db):
        self.window = window
        self.db = db
        self._alarm_ids = []

    def refresh(self):
        alarms = self.db.get_alarms()
        self._alarm_ids = [row[0] for row in alarms]
        entries = [f"{row[2]} {row[3]} - {row[1]}" for row in alarms]
        self.window["-COL-"].update(values=entries)

    def add(self, name, date, time, desc="No description"):
        self.db.add_alarm(name, date, time, desc)
        self.refresh()

    def delete(self, alarm_id):
        self.db.delete_alarm(alarm_id)
        self.refresh()

    def get_alarm_id_at(self, index):
        return self._alarm_ids[index]

    def get_alarm_by_id(self, alarm_id):
        alarms = self.db.get_alarms()
        return next(row for row in alarms if row[0] == alarm_id)
