
class Slot:
    """
    day
    1 = monday
    2 = tuesday
    3 = wednesday
    4 = thursday
    5 = friday
    6 = saturday
    7 = sunday
    --------------
    time
    1 = 8AM
    2 = 9AM
    3 = 10AM
    4 = 11AM
    5 = 12PM
    6 = 1PM
    7 = 2PM
    8 = 3PM
    9 = 4PM
    10 = 5PM
    11 = 6PM
    """
    def __init__(self, day, start_time, end_time):
        assert isinstance(day, int), "day must be a int"
        assert isinstance(start_time, int), "start time must be a int"
        assert isinstance(end_time, int), "end time must be a int"
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        time = ["8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM"]
        return f'{days[self.day-1]} {time[self.start_time-1]}'
