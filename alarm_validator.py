import datetime
import FreeSimpleGUI as gf


class AlarmValidator:
    @staticmethod
    def make_warning(key):
        return gf.Text("⚠ Required", key=key, text_color="red", background_color="black",
                       font=("Helvetica", 9), visible=False)

    @staticmethod
    def validate_inputs(date_str, time_str):
        errors = {}
        try:
            datetime.datetime.strptime(date_str.strip(), "%m/%d/%Y")
        except ValueError:
            errors["input_date"] = "⚠ Invalid date (MM/DD/YYYY)"
        try:
            datetime.datetime.strptime(time_str.strip(), "%H:%M")
        except ValueError:
            errors["input_time"] = "⚠ Invalid time (HH:MM)"
        return errors