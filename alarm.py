import sys

from configuration import Configuration
from screen import Screen

import FreeSimpleGUI as gf

class AlarmScreen(Screen):
    def __init__(self):
        self.nav_buttons = [
            gf.Button("Alarms", key="-ALARMS-", button_color=("white", "purple"), pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Stopwatch", key="-STOPWATCH-", button_color=("white", "black"), pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Calendar", key="-CALENDAR-", button_color=("white", "black"), pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
        ]

        alarms_view = gf.Column([
            [gf.Text("Alarms", justification="left", expand_x=True, font=("Helvetica", 20, "bold"), background_color="black"),
             gf.Button("+", key="add-alarm", font=("Helvetica", 20), button_color=("white", "black"), border_width=0, mouseover_colors=("gray", "black"))],
            [gf.Column([], key="-COL-", background_color="gray", expand_x=True)]
        ], key="-VIEW-ALARMS-", background_color="black", expand_x=True, visible=True)

        stopwatch_view = gf.Column([
            [gf.Text("Stopwatch", justification="center", expand_x=True, font=("Helvetica", 20, "bold"), background_color="black")],
            [gf.Text("00:00:00", key="-STOPWATCH-DISPLAY-", justification="center", expand_x=True, font=("Helvetica", 48, "bold"), background_color="black")],
            [gf.Column([
                [gf.Button("Start", key="-SW-START-", button_color=("white", "green"), font=("Helvetica", 12), border_width=0),
                 gf.Button("Stop", key="-SW-STOP-", button_color=("white", "red"), font=("Helvetica", 12), border_width=0),
                 gf.Button("Reset", key="-SW-RESET-", button_color=("white", "black"), font=("Helvetica", 12), border_width=0)]
            ], element_justification="center", expand_x=True, background_color="black")]
        ], key="-VIEW-STOPWATCH-", background_color="black", expand_x=True, visible=False)

        calendar_view = gf.Column([
            [gf.Text("Calendar", justification="center", expand_x=True, font=("Helvetica", 20, "bold"), background_color="black")],
            [gf.Column([
                [gf.Text("Sun", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Mon", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Tue", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Wed", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Thu", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Fri", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold")),
                 gf.Text("Sat", expand_x=True, justification="center", background_color="#222", font=("Helvetica", 10, "bold"))],
                *self._build_calendar_rows()
            ], expand_x=True, background_color="black")]
        ], key="-VIEW-CALENDAR-", background_color="black", expand_x=True, visible=False)

        super().__init__("Alarms", layout=[
            [gf.Column([self.nav_buttons], background_color="black", expand_x=True, pad=(0, 0), element_justification='center')],
            [gf.HorizontalSeparator()],
            # Single row holds all views — only one visible at a time
            [alarms_view, stopwatch_view, calendar_view],
        ])

        self.counter = 1
        self.stopwatch_running = False
        self.stopwatch_seconds = 0
        self.add_button()

    def show_view(self, view_key):
        for key in ["-VIEW-ALARMS-", "-VIEW-STOPWATCH-", "-VIEW-CALENDAR-"]:
            self.window[key].update(visible=(key == view_key))

    def toggle_selection(self, key):
        for button in self.nav_buttons:
            if key == button.key:
                self.window[button.key].update(button_color=("white", "purple"))
            else:
                self.window[button.key].update(button_color=("white", "black"))

    def add_button(self, iterations=1, name="Dentist Appointment", date="02/09/2026"):
        buttons_to_add = []
        for i in range(iterations):
            button = gf.Button(f"{name} - {date}", key=f"alarm-{self.counter}", font=("Helvetica", 12), button_color=("white", "black"), border_width=0, mouseover_colors=("gray", "black"), expand_x=True)
            buttons_to_add.append(button)
            self.counter += 1
        self.window.extend_layout(self.window["-COL-"], [buttons_to_add])

    def _build_calendar_rows(self):
        import calendar
        import datetime
        now = datetime.datetime.now()
        cal = calendar.monthcalendar(now.year, now.month)
        rows = []
        for week in cal:
            row = []
            for day in week:
                label = str(day) if day != 0 else ""
                is_today = (day == now.day)
                color = "purple" if is_today else "black"
                row.append(gf.Text(label, expand_x=True, justification="center", background_color=color, font=("Helvetica", 10), pad=(2, 4)))
            rows.append(row)
        return rows

    def _format_time(self, centiseconds):
        total_seconds = centiseconds // 100
        cs = centiseconds % 100
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02}:{m:02}:{s:02}.{cs:02}"

    def initialize_ui(self):
        current_window = self.window
        while True:
            timeout = 10 if self.stopwatch_running else None
            event, values = current_window.read(timeout=timeout)

            if event == gf.TIMEOUT_EVENT and self.stopwatch_running:
                self.stopwatch_seconds += 1
                self.window["-STOPWATCH-DISPLAY-"].update(self._format_time(self.stopwatch_seconds))

            elif event == "add-alarm":
                self.config()

            elif event in ("-ALARMS-", "-STOPWATCH-", "-CALENDAR-"):
                self.toggle_selection(event)
                view_map = {
                    "-ALARMS-": "-VIEW-ALARMS-",
                    "-STOPWATCH-": "-VIEW-STOPWATCH-",
                    "-CALENDAR-": "-VIEW-CALENDAR-",
                }
                self.show_view(view_map[event])

            elif event == "-SW-START-":
                self.stopwatch_running = True

            elif event == "-SW-STOP-":
                self.stopwatch_running = False

            elif event == "-SW-RESET-":
                self.stopwatch_running = False
                self.stopwatch_seconds = 0
                self.window["-STOPWATCH-DISPLAY-"].update("00:00:00.00")

            elif event == gf.WIN_CLOSED:
                self.exit()

    def config(self):
        def make_warning(key):
            return gf.Text("⚠ Required", key=key, text_color="red", background_color="black",
                           font=("Helvetica", 9), visible=False)

        config_layout = [
            [gf.Text("Set Alarm", justification="center", font=("Helvetica", 15, "bold"), background_color="black")],
            [gf.Push(background_color="black")],

            [gf.Text("Name:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_name", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), make_warning("-WARN-NAME-")],

            [gf.Text("Date:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_date", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), make_warning("-WARN-DATE-")],

            [gf.Text("Time:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_time", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), make_warning("-WARN-TIME-")],

            [gf.Text("Description:", font=("Helvetica", 12), background_color="black")],
            [gf.Multiline(key="input_desc", font=("Helvetica", 12), expand_x=True, expand_y=True)],

            [gf.Push(background_color="black")],
            [gf.Push(background_color="black"),
             gf.Button("Save", button_color=("white", "black"), font=("Helvetica", 12), border_width=0,
                       mouseover_colors=("gray", "black")),
             gf.Button("Cancel", button_color=("white", "black"), font=("Helvetica", 12), border_width=0,
                       mouseover_colors=("gray", "black")),
             gf.Push(background_color="black")]
        ]

        config_window = gf.Window("Add Alarm", config_layout, modal=True, background_color="black")

        while True:
            event, values = config_window.read()

            if event == gf.WIN_CLOSED or event == "Cancel":
                config_window.close()
                return

            if event == "Save":
                # Validate required fields
                required = {
                    "input_name": "-WARN-NAME-",
                    "input_date": "-WARN-DATE-",
                    "input_time": "-WARN-TIME-",
                }

                has_error = False
                for field, warn_key in required.items():
                    is_empty = not values[field].strip()
                    config_window[warn_key].update(visible=is_empty)
                    if is_empty:
                        has_error = True

                if not has_error:
                    config_window.close()
                    self.add_button(name=values["input_name"], date=values["input_date"])
                    return