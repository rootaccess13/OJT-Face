from datetime import datetime

class Decider:
    def __init__(self):
        self.present_start = datetime.strptime("08:00 AM", "%I:%M %p").time()
        self.present_end = datetime.strptime("08:30 AM", "%I:%M %p").time()
        self.late_end = datetime.strptime("12:00 PM", "%I:%M %p").time()
        self.halfday_end = datetime.strptime("05:00 PM", "%I:%M %p").time()

    def decide(self, time_str):
        time = datetime.strptime(time_str, "%I:%M %p").time()
        if time >= self.present_start and time <= self.present_end:
            return "Present"
        elif time <= self.late_end:
            return "Late"
        elif time <= self.halfday_end:
            return "Half Day"
        else:
            return "Absent"

    def checkDateDiff(self, date):
        today = datetime.now().strftime("%Y-%m-%d")
        frmt_today = datetime.strptime(today, "%Y-%m-%d")
        date = datetime.strptime(date, "%Y-%m-%d")
        diff = date - frmt_today
        return diff.days
