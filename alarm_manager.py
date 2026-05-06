import datetime
import threading
import winsound
from pathlib import Path

class AlarmManager:
    def __init__(self, window, db):
        self.window = window
        self.db = db
        self._alarm_ids = []
        self._triggered = set()  # tracks alarm ids that have already fired
        self._stop_sound = threading.Event()
        self._sound_thread = None

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
        self._triggered.discard(alarm_id)  # clear trigger state if deleted
        self.refresh()

    def get_alarm_id_at(self, index):
        return self._alarm_ids[index]

    def get_alarm_by_id(self, alarm_id):
        alarms = self.db.get_alarms()
        return next(row for row in alarms if row[0] == alarm_id)

    def check_alarms(self):
        now = datetime.datetime.now()
        current_dt_str = now.strftime("%Y-%m-%d %H:%M")

        for alarm in self.db.get_alarms():
            alarm_id = alarm[0]
            title = alarm[1]
            alarm_date = alarm[2]
            alarm_time = alarm[3]
            description = alarm[4] or ""

            try:
                parsed_date = datetime.datetime.strptime(alarm_date, "%m/%d/%Y")
            except ValueError:
                try:
                    parsed_date = datetime.datetime.strptime(alarm_date, "%Y-%m-%d")
                except ValueError:
                    continue

            alarm_dt_str = f"{parsed_date.strftime('%Y-%m-%d')} {alarm_time[:5]}"

            print(f"{alarm_dt_str} == {current_dt_str} {alarm_dt_str == current_dt_str}")
            if alarm_dt_str == current_dt_str and alarm_id not in self._triggered:
                self._triggered.add(alarm_id)
                self._fire(alarm_id, title, description)

    def _fire(self, alarm_id, title, description):
        """Play sound and show popup for a triggered alarm."""
        self._play_alarm_sound()
        import FreeSimpleGUI as gf
        gf.popup(
            f"{title}\n\n{description}",
            title="Alarm",
            background_color="black",
            text_color="white",
            button_color=("white", "purple"),
            font=("Helvetica", 14),
            keep_on_top=True
        )
        self._stop_alarm_sound()
        self.db.deactivate_alarm(alarm_id)
        self.refresh()

    def _play_alarm_sound(self):
        self._stop_sound.clear()
        self._sound_thread = threading.Thread(target=self._sound_loop, daemon=True)
        self._sound_thread.start()

    def _stop_alarm_sound(self):
        self._stop_sound.set()

    def _sound_loop(self):
        SOUND_FILE = Path(__file__).parent / "sounds/alarm_sound.wav"
        while not self._stop_sound.is_set():
            winsound.PlaySound(str(SOUND_FILE), winsound.SND_FILENAME)