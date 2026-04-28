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
            #gf.Button("Contact", key="-CONTACT-", button_color=("white", "black"), pad=(10, 0), font=("Helvetica", 10, "bold"), border_width=0),
        ]
        super().__init__("Alarms", layout = [
            [gf.Column([self.nav_buttons], background_color="black", expand_x=True, pad=(0, 0), element_justification='center')],
            [gf.HorizontalSeparator()],
            [gf.Text("Alarms", justification="left", expand_x=True, font=("Helvetica", 20, "bold"),background_color="black"),
             gf.Button("+", key="add-alarm", font=("Helvetica", 20), button_color=("white", "black"), border_width=0, mouseover_colors=("gray", "black"))],
             [
                 gf.Column([], key="-COL-", background_color="gray", expand_x=True)
             ]
        ])
        self.counter = 1
        self.add_button()

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
            self.counter = self.counter + 1
            print(self.counter)
        self.window.extend_layout(self.window["-COL-"], [buttons_to_add])

    def initialize_ui(self):
        current_window = self.window
        while True:
            event, values = current_window.read()
            if event == "add-alarm":
                self.config()
            if event == "-ALARMS-" or event == "-STOPWATCH-" or event == "-CALENDAR-":
                self.toggle_selection(event)
            if event == gf.WIN_CLOSED:
                self.exit()

    def config(self):

        config_layout = [

            [gf.Text("Set Alarm", justification="center", font=("Helvetica", 15, "bold"), background_color="black")],
            [gf.Push(background_color="black")],
            [gf.Text("Name:", justification="center", font=("Helvetica", 12), background_color="black"), gf.Input(key="input_name", font=("Helvetica", 12), expand_x=True)],
            [gf.Text("Date:", justification="center", font=("Helvetica", 12), background_color="black"), gf.Input(key="input_date", font=("Helvetica", 12), expand_x=True)],
            [gf.Text("Time:", justification="center", font=("Helvetica", 12), background_color="black"), gf.Input(key="input_time", font=("Helvetica", 12), expand_x=True)],
            [gf.Text("Description:", justification="center", font=("Helvetica", 12), background_color="black", expand_y=True)],
            [gf.Multiline(key="input_desc", font=("Helvetica", 12), expand_x=True, expand_y=True)],
            [gf.Push(background_color="black")],
            [gf.Push(background_color="black"),
                 gf.Button("Save", button_color=("white", "black"), font=("Helvetica", 12), border_width=0, mouseover_colors=("gray", "black")),
                 gf.Button("Cancel", button_color=("white", "black"), font=("Helvetica", 12), border_width=0, mouseover_colors=("gray", "black")),
                 gf.Push(background_color="black")
            ]
        ]

        config_window = gf.Window("Add Alarm", config_layout, modal=True, background_color="black")
        event, values = config_window.read()
        config_window.close()
        if event == "Save":
            self.add_button(name=values["input_name"], date=values["input_date"])
        elif event == gf.WIN_CLOSED or event == "Cancel":
            return





        

