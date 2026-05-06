from screen import Screen
from timer import Timer
from database import Database
from alarm_manager import AlarmManager
from alarm_config_dialog import AlarmConfigDialog
from stopwatch_controller import StopwatchController
from calendar_controller import CalendarController
import FreeSimpleGUI as gf


class AlarmScreen(Screen):
    def __init__(self):
        self.nav_buttons = [
            gf.Button("Alarms",    key="-ALARMS-",    button_color=("white", "purple"), pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Timer",     key="-TIMER-",     button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Stopwatch", key="-STOPWATCH-", button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
            gf.Button("Calendar",  key="-CALENDAR-",  button_color=("white", "black"),  pad=(10, 5), font=("Helvetica", 10, "bold"), border_width=0),
        ]

        alarms_view = gf.Column([
            [gf.Text("Alarms", justification="left", expand_x=True, font=("Helvetica", 20, "bold"),
                     background_color="black"),
             gf.Button("+", key="add-alarm", font=("Helvetica", 20), button_color=("white", "black"),
                       border_width=0, mouseover_colors=("gray", "black")),
             gf.Button("−", key="delete-alarm", font=("Helvetica", 20), button_color=("white", "black"),
                       border_width=0, mouseover_colors=("gray", "black"))],
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
                [gf.Button("Start", key="-TM-START-", button_color=("white", "green"),  font=("Helvetica", 12), border_width=0),
                 gf.Button("Pause", key="-TM-PAUSE-", button_color=("white", "orange"), font=("Helvetica", 12), border_width=0),
                 gf.Button("Reset", key="-TM-RESET-", button_color=("white", "black"),  font=("Helvetica", 12), border_width=0)]
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

        calendar_view = gf.Column([
            [gf.Text("Calendar", justification="center", expand_x=True,
                     font=("Helvetica", 20, "bold"), background_color="black")],
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

        self.timer     = Timer(self.window)
        self.db        = Database()
        self.alarms    = AlarmManager(self.window, self.db)
        self.stopwatch = StopwatchController(self.window)
        self.calendar  = CalendarController(self.window, self.db)
        self.dialog    = AlarmConfigDialog(on_save=self.alarms.add)

        self.alarms.refresh()
        self.window["-COL-"].bind("<Double-Button-1>", "-DOUBLE-")

    def show_view(self, view_key):
        for key in ["-VIEW-ALARMS-", "-VIEW-TIMER-", "-VIEW-STOPWATCH-", "-VIEW-CALENDAR-"]:
            self.window[key].update(visible=(key == view_key))

    def toggle_selection(self, key):
        for button in self.nav_buttons:
            color = "purple" if key == button.key else "black"
            self.window[button.key].update(button_color=("white", color))

    # --- Main loop ---

    def initialize_ui(self):
        while True:
            timeout = 10 if (self.stopwatch.running or self.timer.is_active) else 100
            event, values = self.window.read(timeout=timeout)

            self.timer.check_popup()

            if event == gf.TIMEOUT_EVENT:
                self.stopwatch.tick()
                self.timer.tick()
                self.alarms.check_alarms()

            elif event in ("-ALARMS-", "-TIMER-", "-STOPWATCH-", "-CALENDAR-"):
                self.toggle_selection(event)
                self.show_view({
                    "-ALARMS-":    "-VIEW-ALARMS-",
                    "-TIMER-":     "-VIEW-TIMER-",
                    "-STOPWATCH-": "-VIEW-STOPWATCH-",
                    "-CALENDAR-":  "-VIEW-CALENDAR-",
                }[event])
                if event == "-CALENDAR-":
                    self.calendar.refresh_list()
                    self.calendar.show_popup()

            elif event == "add-alarm":
                self.dialog.open()

            elif event == "delete-alarm":
                selected = values["-COL-"]
                if selected:
                    idx = self.window["-COL-"].get_list_values().index(selected[0])
                    alarm_id = self.alarms.get_alarm_id_at(idx)
                    confirm = gf.popup_yes_no(
                        "Delete this alarm?",
                        title="Confirm Delete",
                        background_color="black", text_color="white",
                        button_color=("white", "purple"),
                        font=("Helvetica", 12), keep_on_top=True
                    )
                    if confirm == "Yes":
                        self.alarms.delete(alarm_id)

            elif event == "-SW-START-": self.stopwatch.start()
            elif event == "-SW-STOP-":  self.stopwatch.stop()
            elif event == "-SW-RESET-": self.stopwatch.reset()

            elif event == "-TM-START-":
                try:
                    self.timer.start(
                        int(values["-TIMER-HH-"] or 0),
                        int(values["-TIMER-MM-"] or 0),
                        int(values["-TIMER-SS-"] or 0),
                    )
                except ValueError:
                    pass
            elif event == "-TM-PAUSE-": self.timer.pause_resume()
            elif event == "-TM-RESET-": self.timer.reset()

            elif event == "-COL--DOUBLE-":
                selected_index = values["-COL-"]
                if selected_index:
                    idx = self.window["-COL-"].get_list_values().index(selected_index[0])
                    alarm = self.alarms.get_alarm_by_id(self.alarms.get_alarm_id_at(idx))
                    gf.popup(
                        f"Name:         {alarm[1]}\nDate:           {alarm[2]}\nTime:           {alarm[3]}\nDescription:  {alarm[4] or ''}",
                        title="Alarm Details",
                        background_color="black", text_color="white",
                        button_color=("white", "purple"),
                        font=("Helvetica", 12), keep_on_top=True
                    )

            elif event == gf.WIN_CLOSED:
                self.exit()
