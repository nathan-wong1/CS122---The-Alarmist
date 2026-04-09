from datetime import datetime
import sys

import FreeSimpleGUI as gf
import base64

class Screen:
    def __init__(self, title, size=(400,300)):
        self.layout = [
            [gf.Text("Alarm", justification="center", expand_x=True, font=("Helvetica", 12, "bold"), background_color="black")],
            [gf.Text("Set an alarm:", background_color="black"),
             gf.InputText(key="time")],
            [gf.Button("Submit"), gf.Button("Cancel")]
        ]
        self.size = size
        self.title = title
        self.window = gf.Window(self.title, self.layout, size=self.size, background_color="black")

        with open("alarm.png", "rb") as f:
            self.icon = base64.b64encode(f.read())

    def initialize_ui(self):
        current_window = self.window
        while True:
            event, values = current_window.read()

            if event == gf.WIN_CLOSED or event == "Cancel":
                self.exit()

            if event == "Submit":
                try:
                    time = values["time"]
                    today = datetime.today().date()
                    gf.popup(datetime.strptime(f"{today} {time}", "%B %d %Y %H:%M"))
                except:
                    gf.popup("Invalid time")


    def exit(self):
        exit_layout = [
            [gf.Text("Are you sure you want to exit?")],
            [gf.Button("Yes"), gf.Button("Cancel")]
        ]
        while True:
            quit_window = gf.Window("Quit Alarm", exit_layout, modal=True)
            event, values = quit_window.read()
            quit_window.close()
            if event == "Yes":
                sys.exit()
            elif event == gf.WIN_CLOSED or event == "Cancel":
                break
            else:
                continue
