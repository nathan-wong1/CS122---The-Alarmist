import FreeSimpleGUI as gf
from alarm_validator import AlarmValidator


class AlarmConfigDialog:
    def __init__(self, on_save):
        """
        on_save: callable(name, date, time, desc) called when the user saves a valid alarm.
        """
        self.on_save = on_save

    def open(self):
        config_layout = [
            [gf.Text("Set Alarm", justification="center", font=("Helvetica", 15, "bold"),
                     background_color="black")],
            [gf.Push(background_color="black")],
            [gf.Text("Name:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_name", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), AlarmValidator.make_warning("-WARN-NAME-")],
            [gf.Text("Date:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_date", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), AlarmValidator.make_warning("-WARN-DATE-")],
            [gf.Text("Time:", font=("Helvetica", 12), background_color="black"),
             gf.Input(key="input_time", font=("Helvetica", 12), expand_x=True)],
            [gf.Push(background_color="black"), AlarmValidator.make_warning("-WARN-TIME-")],
            [gf.Text("Description:", font=("Helvetica", 12), background_color="black")],
            [gf.Multiline(key="input_desc", font=("Helvetica", 12), expand_x=True, expand_y=True)],
            [gf.Push(background_color="black")],
            [gf.Push(background_color="black"),
             gf.Button("Save",   button_color=("white", "black"), font=("Helvetica", 12),
                       border_width=0, mouseover_colors=("gray", "black")),
             gf.Button("Cancel", button_color=("white", "black"), font=("Helvetica", 12),
                       border_width=0, mouseover_colors=("gray", "black")),
             gf.Push(background_color="black")]
        ]

        window = gf.Window("Add Alarm", config_layout, modal=True, background_color="black")
        required = {"input_name": "-WARN-NAME-", "input_date": "-WARN-DATE-", "input_time": "-WARN-TIME-"}

        while True:
            event, values = window.read()

            if event in (gf.WIN_CLOSED, "Cancel"):
                window.close()
                return

            if event == "Save":
                # Reset warnings
                for warn_key in required.values():
                    window[warn_key].update(visible=False, value="⚠ Required")

                has_error = False

                for field, warn_key in required.items():
                    if not values[field].strip():
                        window[warn_key].update(value="⚠ Required", visible=True)
                        has_error = True

                if values["input_date"].strip() and values["input_time"].strip():
                    format_errors = AlarmValidator.validate_inputs(
                        values["input_date"], values["input_time"]
                    )
                    for field, message in format_errors.items():
                        window[required[field]].update(value=message, visible=True)
                        has_error = True

                if not has_error:
                    window.close()
                    self.on_save(
                        values["input_name"],
                        values["input_date"],
                        values["input_time"],
                        values["input_desc"]
                    )
                    return
