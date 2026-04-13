from datetime import datetime
import sys

import FreeSimpleGUI as gf
import base64

class Screen:
    def __init__(self, title, icon="icon/alarm.png", layout=None, size=(400, 300)):
        if layout is None:
            layout = []
        self.layout = layout

        with open(icon, "rb") as f:
            self.icon = base64.b64encode(f.read())
        self.size = size
        self.title = title
        self.window = gf.Window(self.title, self.layout, size=self.size, icon=self.icon, background_color="black", finalize=True)

    def initialize_ui(self):
        current_window = self.window
        while True:
            event, values = current_window.read()
            if event == gf.WIN_CLOSED:
                self.exit()

    def change_layout(self, layout):
        self.layout = layout

    def exit(self):
        exit_layout = [
            [gf.Text("Are you sure you want to exit?", background_color="black")],
            [gf.Button("Yes"), gf.Button("Cancel")]
        ]
        while True:
            quit_window = gf.Window("Quit Alarm", exit_layout, modal=True, background_color="black")
            event, values = quit_window.read()
            quit_window.close()
            if event == "Yes":
                sys.exit()
            elif event == gf.WIN_CLOSED or event == "Cancel":
                break
            else:
                continue