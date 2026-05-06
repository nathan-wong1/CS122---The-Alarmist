class StopwatchController:
    def __init__(self, window):
        self.window = window
        self.running = False
        self.centiseconds = 0

    def tick(self):
        if self.running:
            self.centiseconds += 1
            self.window["-STOPWATCH-DISPLAY-"].update(self._format())

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.centiseconds = 0
        self.window["-STOPWATCH-DISPLAY-"].update("00:00:00.00")

    def _format(self):
        total_seconds = self.centiseconds // 100
        cs = self.centiseconds % 100
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02}:{m:02}:{s:02}.{cs:02}"
