import calendar
import datetime
import FreeSimpleGUI as gf


class CalendarController:
    def __init__(self, window, db):
        self.window = window
        self.db = db
        now = datetime.datetime.now()
        self._cal_year  = now.year
        self._cal_month = now.month

    def refresh_list(self):
        """Updates the embedded -CAL-LIST- listbox with alarms for the current month."""
        now = datetime.datetime.now()
        self.window["-CAL-MONTH-LABEL-"].update(now.strftime("%B %Y"))

        alarms = self.db.get_alarms()
        entries = []
        for row in alarms:
            try:
                d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                if d.year == now.year and d.month == now.month:
                    entries.append(f"{row[2]} {row[3]} - {row[1]}")
            except ValueError:
                pass

        self.window["-CAL-LIST-"].update(values=entries if entries else ["No alarms this month."])

    def show_popup(self, year=None, month=None):
        """Opens a navigable calendar popup with alarm indicators."""
        now = datetime.datetime.now()
        year  = year  or self._cal_year
        month = month or self._cal_month

        layout, alarm_days = self._build_popup_layout(year, month, now)
        popup = gf.Window("Calendar", layout, modal=True, background_color="black",
                          keep_on_top=True, finalize=True)

        while True:
            ev, _ = popup.read()

            if ev == gf.WIN_CLOSED:
                break

            elif ev == "-CP-PREV-":
                month -= 1
                if month < 1:
                    month, year = 12, year - 1
                popup.close()
                self._cal_year, self._cal_month = year, month
                self.show_popup(year, month)
                return

            elif ev == "-CP-NEXT-":
                month += 1
                if month > 12:
                    month, year = 1, year + 1
                popup.close()
                self._cal_year, self._cal_month = year, month
                self.show_popup(year, month)
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

    def _build_popup_layout(self, year, month, now):
        alarms = self.db.get_alarms()
        alarm_days = {}
        for row in alarms:
            try:
                d = datetime.datetime.strptime(row[2].strip(), "%d/%m/%Y")
                if d.year == year and d.month == month:
                    alarm_days.setdefault(d.day, []).append(row)
            except ValueError:
                pass

        month_label = datetime.date(year, month, 1).strftime("%B %Y")

        header_row = [[
            gf.Button("◀", key="-CP-PREV-", button_color=("white", "black"),
                      font=("Helvetica", 12), border_width=0),
            gf.Text(month_label, justification="center", expand_x=True,
                    font=("Helvetica", 14, "bold"), background_color="black"),
            gf.Button("▶", key="-CP-NEXT-", button_color=("white", "black"),
                      font=("Helvetica", 12), border_width=0),
        ]]

        day_headers = [[
            gf.Text(d, expand_x=True, justification="center", background_color="#222",
                    font=("Helvetica", 10, "bold"), size=(4, 1))
            for d in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        ]]

        day_rows = []
        for week in calendar.monthcalendar(year, month):
            row = []
            for day in week:
                if day == 0:
                    row.append(gf.Text("", expand_x=True, size=(4, 2),
                                       background_color="black", font=("Helvetica", 10)))
                else:
                    is_today  = (day == now.day and year == now.year and month == now.month)
                    has_alarm = day in alarm_days
                    bg = "purple" if is_today else ("#5a0000" if has_alarm else "#1a1a1a")
                    row.append(gf.Button(
                        f"{day}\n{'●' if has_alarm else ''}",
                        key=f"-CP-DAY-{day}-",
                        button_color=("white", bg),
                        font=("Helvetica", 9), size=(4, 2), border_width=0,
                        mouseover_colors=("white", "#333")
                    ))
            day_rows.append(row)

        legend = [[
            gf.Text("■", text_color="purple",  background_color="black", font=("Helvetica", 9)),
            gf.Text("Today",     background_color="black", font=("Helvetica", 9), text_color="gray"),
            gf.Text("  ■", text_color="#5a0000", background_color="black", font=("Helvetica", 9)),
            gf.Text("Has alarm", background_color="black", font=("Helvetica", 9), text_color="gray"),
        ]]

        return header_row + day_headers + day_rows + legend, alarm_days
