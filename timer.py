import threading
import winsound
import FreeSimpleGUI as gf


class Timer:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.remaining = 0
        self._tick_accum = 0
        self._alarm_active = False
        self._show_alarm_popup = False

    def start(self, hh, mm, ss):
        total = hh * 3600 + mm * 60 + ss
        if total <= 0:
            return False
        self.remaining = total
        self._tick_accum = 0
        self.running = True
        self.window["-TIMER-DONE-"].update(visible=False)
        self.window["-TIMER-INPUTS-"].update(visible=False)
        self.window["-TIMER-DISPLAY-"].update(self._format(self.remaining))
        self.window["-TIMER-DISPLAY-COL-"].update(visible=True)
        return True

    def pause_resume(self):
        self.running = not self.running
        self.window["-TM-PAUSE-"].update(text="Resume" if not self.running else "Pause")

    def reset(self):
        self.running = False
        self.remaining = 0
        self._tick_accum = 0
        self._alarm_active = False
        self._show_alarm_popup = False
        self.window["-TIMER-DISPLAY-COL-"].update(visible=False)
        self.window["-TIMER-DONE-"].update(visible=False)
        self.window["-TM-PAUSE-"].update(text="Pause")
        self.window["-TIMER-INPUTS-"].update(visible=True)
        self.window["-TIMER-HH-"].update("00")
        self.window["-TIMER-MM-"].update("00")
        self.window["-TIMER-SS-"].update("00")

    def tick(self):
        """Call every 10ms. Returns True if alarm should fire."""
        if not self.running:
            return False
        self._tick_accum += 1
        if self._tick_accum >= 100:
            self._tick_accum = 0
            self.remaining -= 1
            self.window["-TIMER-DISPLAY-"].update(self._format(self.remaining))
            if self.remaining <= 0:
                self.running = False
                self.window["-TIMER-DONE-"].update("⏰ Time's up!", visible=True)
                self._alarm_active = True
                self._show_alarm_popup = True
                threading.Thread(target=self._play_sound, daemon=True).start()
                return True
        return False

    def check_popup(self):
        """Call from main thread each loop iteration."""
        if self._show_alarm_popup:
            self._show_alarm_popup = False
            gf.popup(
                "⏰ Time's Up!",
                title="Timer Alarm",
                button_color=("white", "purple"),
                background_color="black",
                text_color="white",
                font=("Helvetica", 18, "bold"),
                keep_on_top=True
            )
            self._alarm_active = False

    def _play_sound(self):
        while self._alarm_active:
            winsound.Beep(1000, 500)

    def _format(self, seconds):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        return f"{h:02}:{m:02}:{s:02}"

    @property
    def is_active(self):
        return self.running or self._alarm_active