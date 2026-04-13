from screen import Screen
import FreeSimpleGUI as gf

class Configuration(Screen):
    def __init__(self):
        super().__init__("Add Alarm", layout=[
            [gf.Text("Configure An Alarm", justification="center", expand_x=True, font=("Helvetica", 20, "bold"),
                     background_color="black"),
             gf.Button("+", key="add-alarm", font=("Helvetica", 20), button_color=("white", "black"), border_width=0,
                       mouseover_colors=("gray", "black"))]
        ])