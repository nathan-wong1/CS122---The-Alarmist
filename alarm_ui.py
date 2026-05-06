from screen import Screen
from timer import Timer
from database import Database

import calendar
import datetime
import FreeSimpleGUI as gf

class AlarmScreen(Screen):
    def __init__(self):
        self.nav_buttons = [
            gf.Button("Alarms",     key="-ALARMS-",    button_color=("white", "purple"), pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Timer",      key="-TIMER-",     button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Stopwatch",  key="-STOPWATCH-", button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Calendar",   key="-CALENDAR-",  button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
        ]

        alarms_view = gf.Column([
            [gf.Text("Alarms", justification="left", expand_x=True, font=("Helvetica", 20, "bold"),
                     background_color="black"),
             gf.Button("+", key="add-alarm", font=("Helvetica", 20), button_color=("white", "black"), border_width=0,
                       mouseover_colors=("gray", "black")),
             gf.Button("−", key="delete-alarm", font=("Helvetica", 20), button_color=("white", "black"), border_width=0,
                       mouseover_colors=("gray", "black"))],
            [gf.Listbox(values=[], key="-COL-", background_color="#111", text_color="white",
                font=("Helvetica", 12), expand_x=True, size=(0, 10), no_scrollbar=False,
                select_mode=gf.LISTBOX_SELECT_MODE_SINGLE, enable_events=True)]
        ], key="-VIEW-ALARMS-", background_color="black", expand_x=True, visible=True)

        timer_view = gf.Column([
            [gf.Text("Timer", justification="center", expand_x=True, font=("Helvetica", 20, "bold"), background_color="black")],
            [
                gf.Column([
                    [
                        gf.Input("00", key="-TIMER-HH-", font=("Helvetica", 36, "bold"), size=(3, 1), justification="center", background_color="#222", text_color="white", border_width=0),
                        gf.Text(":", font=("Helvetica", 36, "bold"), background_color="black"),
                        gf.Input("00", key="-TIMER-MM-", font=("Helvetica", 36, "bold"), size=(3, 1), justification="center", background_color="#222", text_color="white", border_width=0),
                        gf.Text(":", font=("Helvetica", 36, "bold"), background_color="black"),
                        gf.Input("00", key="-TIMER-SS-", font=("Helvetica", 36, "bold"), size=(3, 1), justification="center", background_color="#222", text_color="white", border_width=0),
                    ],
                    [
                        gf.Text("HH", expand_x=True, justification="center", background_color="black", font=("Helvetica", 9), text_color="gray"),
                        gf.Text("",   background_color="black", font=("Helvetica", 9)),
                        gf.Text("MM", expand_x=True, justification="center", background_color="black", font=("Helvetica", 9), text_color="gray"),
                        gf.Text("",   background_color="black", font=("Helvetica", 9)),
                        gf.Text("SS", expand_x=True, justification="center", background_color="black", font=("Helvetica", 9), text_color="gray"),
                    ],
                ], key="-TIMER-INPUTS-", element_justification="center", expand_x=True, background_color="black", visible=True),

                gf.Column([
                    [gf.Text("00:00:00", key="-TIMER-DISPLAY-", justification="center", expand_x=True, font=("Helvetica", 48, "bold"), background_color="black")],
                ], key="-TIMER-DISPLAY-COL-", element_justification="center", expand_x=True, background_color="black", visible=False),
            ],
            [gf.Text("", key="-TIMER-DONE-", justification="center", expand_x=True, font=("Helvetica", 14, "bold"), background_color="black", text_color="red", visible=False)],
            [gf.Column([
                [gf.Button("Start",  key="-TM-START-", button_color=("white", "green"),  font=("Helvetica", 12), border_width=0),
                 gf.Button("Pause",  key="-TM-PAUSE-", button_color=("white", "orange"), font=("Helvetica", 12), border_width=0),
                 gf.Button("Reset",  key="-TM-RESET-", button_color=("white", "black"),  font=("Helvetica", 12), border_width=0)]
            ], element_justification="center", expand_x=True, background_color="black")]
        ], key="-VIEW-TIMER-", background_color="black", expand_x=True, visible=False)

        stopwatch_view = gf.Column([
            [gf.Text("Stopwatch", justification="center", expand_x=True, font=("Helvetica", 20, "bold"), background_color="black")],
            [gf.Text("00:00:00.00", key="-STOPWATCH-DISPLAY-", justification="center", expand_x=True, font=("Helvetica", 48, "bold"), background_color="black")],
            [gf.Column([
                [gf.Button("Start", key="-SW-START-", button_color=("white", "green"), font=("Helvetica", 12), border_width=0),
                 gf.Button("Stop",  key="-SW-STOP-",  button_color=("white", "red"),   font=("Helvetica", 12), border_width=0),
                 gf.Button("Reset", key="-SW-RESET-", button_color=("white", "black"), font=("Helvetica", 12), border_width=0)]
            ], element_justification="center", expand_x=True, background_color="black")]
        ], key="-VIEW-STOPWATCH-", background_color="black", expand_x=True, visible=False)



        now = datetime.datetime.now()
        self._cal_year = now.year
        self._cal_month = now.month

        calendar_view = calendar_view = gf.Column([
            [gf.Text("", key="-CAL-MONTH-LABEL-", justification="center", expand_x=True,
                     font=("Helvetica", 13, "bold"), background_color="black")],
            [gf.Listbox(values=[], key="-CAL-LIST-", background_color="#111", text_color="white",
                        font=("Helvetica", 12), expand_x=True, size=(0, 10), no_scrollbar=False,
                        select_mode=gf.LISTBOX_SELECT_MODE_SINGLE, enable_events=True)],
        ], key="-VIEW-CALENDAR-", background_color="black", expand_x=True, visible=False)

        super().__init__("Alarms", layout=[
            [gf.Column([self.nav_buttons], background_color="black", expand_x=True, pad=(0, 0), element_justification='center')],
            [gf.HorizontalSeparator()],
            [alarms_view, timer_view, stopwatch_view, calendar_view],
        ])

        self.stopwatch_running = False
        self.stopwatch_centiseconds = 0
        self.timer = Timer(self.window)

        self.db = Database()
        self._alarm_ids = []
        self.refresh_alarms()

        self.window["-COL-"].bind("<Double-Button-1>", "-DOUBLE-")

    def show_view(self, view_key):
        for key in ["-VIEW-ALARMS-", "-VIEW-TIMER-", "-VIEW-STOPWATCH-", "-VIEW-CALENDAR-"]:
            self.window[key].update(visible=(key == view_key))

    def toggle_selection(self, key):
        for button in self.nav_buttons:
            color = "purple" if key == button.key else "black"
            self.window[button.key].update(button_color=("white", color))

    def add_element(self, name, date, time, desc="No description"):
        self.db.add_alarm(name, date, time, desc)
        self.refresh_alarms()

    def refresh_alarms(self):
        alarms = self.db.get_alarms()
        self._alarm_ids = [row[0] for row in alarms]
        entries = [f"{row[2]} {row[3]} - {row[1]}" for row in alarms]
        self.window["-COL-"].update(values=entries)

    def _build_calendar_rows(self, year=None, month=None):
        now = datetime.datetime.now()
        year = year or now.year
        month = month or now.month
        cal = calendar.monthcalendar(year, month)
        rows = []

        alarms = self.db.get_alarms() if hasattr(self, 'db') else []
        alarm_days = set()
        for row in alarms:
            try:
                d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                if d.year == year and d.month == month:
                    alarm_days.add(d.day)
            except ValueError:
                pass

        for week in cal:
            row = []
            for day in week:
                label = str(day) if day != 0 else ""
                if day != 0 and day == now.day and year == now.year and month == now.month:
                    color = "purple"
                elif day in alarm_days:
                    color = "#8B0000"  # dark red = has alarm
                else:
                    color = "black"
                row.append(gf.Text(
                    label, key=f"-CAL-DAY-{day}-" if day != 0 else f"-CAL-EMPTY-{week.index(day)}-{month}-",
                    expand_x=True, justification="center",
                    background_color=color, font=("Helvetica", 10),
                    pad=(2, 4), enable_events=(day != 0)
                ))
            rows.append(row)
        return rows

    def _format_stopwatch(self, centiseconds):
        total_seconds = centiseconds // 100
        cs = centiseconds % 100
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        return f"{h:02}:{m:02}:{s:02}.{cs:02}"


    def initialize_ui(self):
        while True:
            timeout = 10 if (self.stopwatch_running or self.timer.is_active) else 100
            event, values = self.window.read(timeout=timeout)

            self.timer.check_popup()

            if event == gf.TIMEOUT_EVENT:
                if self.stopwatch_running:
                    self.stopwatch_centiseconds += 1
                    self.window["-STOPWATCH-DISPLAY-"].update(self._format_stopwatch(self.stopwatch_centiseconds))
                self.timer.tick()

            elif event in ("-ALARMS-", "-TIMER-", "-STOPWATCH-", "-CALENDAR-"):
                self.toggle_selection(event)
                self.show_view({
                    "-ALARMS-":    "-VIEW-ALARMS-",
                    "-TIMER-":     "-VIEW-TIMER-",
                    "-STOPWATCH-": "-VIEW-STOPWATCH-",
                    "-CALENDAR-":  "-VIEW-CALENDAR-",
                }[event])
                if event == "-CALENDAR-":
                    self.refresh_calendar_list()
                    self._show_calendar_popup()

            elif event == "add-alarm":
                self.config()

            elif event == "delete-alarm":
                selected = values["-COL-"]
                if selected:
                    idx = self.window["-COL-"].get_list_values().index(selected[0])
                    alarm_id = self._alarm_ids[idx]
                    confirm = gf.popup_yes_no(
                        "Delete this alarm?",
                        title="Confirm Delete",
                        background_color="black",
                        text_color="white",
                        button_color=("white", "purple"),
                        font=("Helvetica", 12),
                        keep_on_top=True
                    )
                    if confirm == "Yes":
                        self.db.delete_alarm(alarm_id)
                        self.refresh_alarms()

            elif event == "-SW-START-":  self.stopwatch_running = True
            elif event == "-SW-STOP-":   self.stopwatch_running = False
            elif event == "-SW-RESET-":
                self.stopwatch_running = False
                self.stopwatch_centiseconds = 0
                self.window["-STOPWATCH-DISPLAY-"].update("00:00:00.00")

            elif event == "-TM-START-":
                try:
                    self.timer.start(
                        int(values["-TIMER-HH-"] or 0),
                        int(values["-TIMER-MM-"] or 0),
                        int(values["-TIMER-SS-"] or 0),
                    )
                except ValueError:
                    pass
            elif event == "-TM-PAUSE-":  self.timer.pause_resume()
            elif event == "-TM-RESET-":  self.timer.reset()

            elif event == "-COL--DOUBLE-":
                selected_index = values["-COL-"]
                if selected_index:
                    idx = self.window["-COL-"].get_list_values().index(selected_index[0])
                    alarm_id = self._alarm_ids[idx]
                    alarms = self.db.get_alarms()
                    alarm = next(row for row in alarms if row[0] == alarm_id)
                    desc_line = f"{alarm[4]}" if alarm[4] else ""
                    gf.popup(
                        f"Name:   {alarm[1]}\nDate:     {alarm[2]}\nTime:     {alarm[3]}\nDescription:  {desc_line}",
                        title="Alarm Details",
                        background_color="black",
                        text_color="white",
                        button_color=("white", "purple"),
                        font=("Helvetica", 12),
                        keep_on_top=True
                    )

            elif event == gf.WIN_CLOSED:
                self.exit()

    def config(self):

        config_layout = [
            [gf.Text("Set Alarm", justification="center", font=("Helvetica", 15, "bold"), background_color="black")],
            [gf.Push(background_color="black")],
            [gf.Text("Name:",        font=("Helvetica", 12), background_color="black"), gf.Input(key="input_name", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), self.make_warning("-WARN-NAME-")],
            [gf.Text("Date:",        font=("Helvetica", 12), background_color="black"), gf.Input(key="input_date", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), self.make_warning("-WARN-DATE-")],
            [gf.Text("Time:",        font=("Helvetica", 12), background_color="black"), gf.Input(key="input_time", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), self.make_warning("-WARN-TIME-")],
            [gf.Text("Description:", font=("Helvetica", 12), background_color="black")],
            [gf.Multiline(key="input_desc", font=("Helvetica", 12), expand_x=True, expand_y=True)],
            [gf.Push(background_color="black")],
            [gf.Push(background_color="black"),
             gf.Button("Save",   button_color=("white", "black"), font=("Helvetica", 12), border_width=0, mouseover_colors=("gray", "black")),
             gf.Button("Cancel", button_color=("white", "black"), font=("Helvetica", 12), border_width=0, mouseover_colors=("gray", "black")),
             gf.Push(background_color="black")]
        ]

        config_window = gf.Window("Add Alarm", config_layout, modal=True, background_color="black")
        while True:
            event, values = config_window.read()
            if event in (gf.WIN_CLOSED, "Cancel"):
                config_window.close()
                return
            if event == "Save":
                required = {"input_name": "-WARN-NAME-", "input_date": "-WARN-DATE-", "input_time": "-WARN-TIME-"}

                # Reset all warnings
                for warn_key in required.values():
                    config_window[warn_key].update(visible=False, value="⚠ Required")

                has_error = False

                # Check empty fields
                for field, warn_key in required.items():
                    if not values[field].strip():
                        config_window[warn_key].update(value="⚠ Required", visible=True)
                        has_error = True

                # Check date/time format only if not already empty
                if values["input_date"].strip() and values["input_time"].strip():
                    format_errors = self.validate_inputs(values["input_date"], values["input_time"])
                    for field, message in format_errors.items():
                        config_window[required[field]].update(value=message, visible=True)
                        has_error = True

                if not has_error:
                    config_window.close()
                    self.add_element(values["input_name"], values["input_date"], values["input_time"], values['input_desc'])
                    return

    def make_warning(self, key):
        return gf.Text("⚠ Required", key=key, text_color="red", background_color="black", font=("Helvetica", 9), visible=False)

    def validate_inputs(self, date_str, time_str):
        errors = {}

        try:
            datetime.datetime.strptime(date_str.strip(), "%d/%m/%Y")
        except ValueError:
            errors["input_date"] = "⚠ Invalid date (DD/MM/YYYY)"

        try:
            datetime.datetime.strptime(time_str.strip(), "%H:%M")
        except ValueError:
            errors["input_time"] = "⚠ Invalid time (HH:MM)"

        return errors

    def refresh_calendar_list(self):
        now = datetime.datetime.now()
        label = now.strftime("%B %Y")
        self.window["-CAL-MONTH-LABEL-"].update(label)

        alarms = self.db.get_alarms()
        entries = []
        for row in alarms:
            try:
                d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                if d.year == now.year and d.month == now.month:
                    entries.append(f"{row[2]} {row[3]} - {row[1]}")
            except ValueError:
                pass

        if not entries:
            entries = ["No alarms this month."]

        self.window["-CAL-LIST-"].update(values=entries)

    def _refresh_calendar(self):
        month_name = datetime.date(self._cal_year, self._cal_month, 1).strftime("%B %Y")
        self.window["-CAL-MONTH-LABEL-"].update(month_name)

        alarms = self.db.get_alarms()
        alarm_days = set()
        for row in alarms:
            try:
                d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                if d.year == self._cal_year and d.month == self._cal_month:
                    alarm_days.add(d.day)
            except ValueError:
                pass

        now = datetime.datetime.now()
        cal = calendar.monthcalendar(self._cal_year, self._cal_month)

        rows = []
        for week in cal:
            row = []
            for day in week:
                label = str(day) if day != 0 else ""
                if day != 0 and day == now.day and self._cal_year == now.year and self._cal_month == now.month:
                    color = "purple"
                elif day in alarm_days:
                    color = "#5a0000"
                else:
                    color = "black"
                row.append(gf.Text(
                    label, expand_x=True, justification="center",
                    background_color=color, font=("Helvetica", 10), pad=(2, 4)
                ))
            rows.append(row)

        header = [[
            gf.Text("Sun", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Mon", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Tue", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Wed", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Thu", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Fri", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
            gf.Text("Sat", expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold")),
        ]]
        self.window["-CAL-GRID-"].widget.destroy()  # remove old grid
        self._show_calendar_popup()

    def _show_calendar_popup(self, year=None, month=None):
        now = datetime.datetime.now()
        year = year or self._cal_year
        month = month or self._cal_month

        def build_layout(y, m):
            alarms = self.db.get_alarms()
            alarm_days = {}
            for row in alarms:
                try:
                    d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                    if d.year == y and d.month == m:
                        alarm_days.setdefault(d.day, []).append(row)
                except ValueError:
                    pass

            cal = calendar.monthcalendar(y, m)
            month_label = datetime.date(y, m, 1).strftime("%B %Y")

            header_row = [[
                gf.Button("◀", key="-CP-PREV-", button_color=("white", "black"), font=("Helvetica", 12),
                          border_width=0),
                gf.Text(month_label, justification="center", expand_x=True,
                        font=("Helvetica", 14, "bold"), background_color="black"),
                gf.Button("▶", key="-CP-NEXT-", button_color=("white", "black"), font=("Helvetica", 12),
                          border_width=0),
            ]]

            day_headers = [[
                gf.Text(d, expand_x=True, justification="center", background_color="#222",
                        font=("Helvetica", 10, "bold"), size=(4, 1))
                for d in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            ]]

            day_rows = []
            for week in cal:
                row = []
                for day in week:
                    if day == 0:
                        row.append(gf.Text("", expand_x=True, size=(4, 2),
                                           background_color="black", font=("Helvetica", 10)))
                    else:
                        is_today = (day == now.day and y == now.year and m == now.month)
                        has_alarm = day in alarm_days
                        bg = "purple" if is_today else ("#5a0000" if has_alarm else "#1a1a1a")
                        indicator = "●" if has_alarm else ""
                        row.append(gf.Button(
                            f"{day}\n{indicator}", key=f"-CP-DAY-{day}-",
                            button_color=("white", bg),
                            font=("Helvetica", 9), size=(4, 2), border_width=0,
                            mouseover_colors=("white", "#333")
                        ))
                day_rows.append(row)

            legend = [[
                gf.Text("■", text_color="purple", background_color="black", font=("Helvetica", 9)),
                gf.Text("Today", background_color="black", font=("Helvetica", 9), text_color="gray"),
                gf.Text("  ■", text_color="#5a0000", background_color="black", font=("Helvetica", 9)),
                gf.Text("Has alarm", background_color="black", font=("Helvetica", 9), text_color="gray"),
            ]]

            return header_row + day_headers + day_rows + legend, alarm_days

        layout, alarm_days = build_layout(year, month)
        popup = gf.Window("Calendar", layout, modal=True, background_color="black",
                          keep_on_top=True, finalize=True)

        while True:
            ev, _ = popup.read()
            if ev == gf.WIN_CLOSED:
                break
            elif ev == "-CP-PREV-":
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                popup.close()
                self._cal_year, self._cal_month = year, month
                self._show_calendar_popup(year, month)
                return
            elif ev == "-CP-NEXT-":
                month += 1
                if month > 12:
                    month = 1
                    year += 1
                popup.close()
                self._cal_year, self._cal_month = year, month
                self._show_calendar_popup(year, month)
                return
            elif ev and ev.startswith("-CP-DAY-"):
                day = int(ev.replace("-CP-DAY-", "").replace("-", ""))
                if day in alarm_days:
                    lines = "\n\n".join(
                        f"🔔 {r[1]}  |  {r[3]}\n   {r[4] or 'No description'}"
                        for r in alarm_days[day]
                    )
                    gf.popup(
                        f"Alarms on {day:02}/{month:02}/{year}:\n\n{lines}",
                        title="Alarms", background_color="black", text_color="white",
                        button_color=("white", "purple"), font=("Helvetica", 11), keep_on_top=True
                    )
                else:
                    gf.popup(
                        f"No alarms on {day:02}/{month:02}/{year}.",
                        title="Alarms", background_color="black", text_color="white",
                        button_color=("white", "purple"), font=("Helvetica", 11), keep_on_top=True
                    )

        popup.close()