import datetime
import threading
import winsound
from pathlib import Path
import FreeSimpleGUI as gf

class Timer:
    def __init__(self, window):
        self.window = window
        self.is_active = False
        self._paused = False
        self._end_time = None
        self._remaining = None
        self._done = False
        self._stop_sound = threading.Event()
        self._sound_thread = None

    def start(self, hh, mm, ss):
        total = hh * 3600 + mm * 60 + ss
        if total <= 0:
            return
        self._remaining = total
        self._end_time = datetime.datetime.now() + datetime.timedelta(seconds=total)
        self.is_active = True
        self._paused = False
        self._done = False
        self._update_display(total)

    def pause_resume(self):
        if not self.is_active:
            return
        if self._paused:
            self._end_time = datetime.datetime.now() + datetime.timedelta(seconds=self._remaining)
            self._paused = False
        else:
            self._remaining = max(0, int((self._end_time - datetime.datetime.now()).total_seconds()))
            self._paused = True

    def reset(self):
        self.is_active = False
        self._paused = False
        self._end_time = None
        self._remaining = None
        self._done = False
        self._stop_alarm_sound()
        self.window["-TIMER-INPUTS-"].update(visible=True)
        self.window["-TIMER-DISPLAY-COL-"].update(visible=False)
        self.window["-TIMER-DONE-"].update(visible=False)

    def tick(self):
        if not self.is_active or self._paused:
            return
        remaining = max(0, int((self._end_time - datetime.datetime.now()).total_seconds()))
        self._update_display(remaining)
        if remaining <= 0:
            self.is_active = False
            self._done = True
            self.window["-TIMER-DONE-"].update("Timer done!", visible=True)

    def check_popup(self):
        if self._done:
            self._done = False
            self._play_alarm_sound()
            gf.popup(
                "Timer finished!",
                title="Timer",
                background_color="black",
                text_color="white",
                button_color=("white", "purple"),
                font=("Helvetica", 14),
                keep_on_top=True
            )
            self._stop_alarm_sound()

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

    def _update_display(self, total_seconds):
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        self.window["-TIMER-INPUTS-"].update(visible=False)
        self.window["-TIMER-DISPLAY-COL-"].update(visible=True)
        self.window["-TIMER-DISPLAY-"].update(f"{h:02}:{m:02}:{s:02}")