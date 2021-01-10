class Slot:
    def __init__(self, day, start_time, end_time):
        assert isinstance(day, str), "day must be a string"
        assert isinstance(start_time, str), "start time must be a string"
        assert isinstance(end_time, str), "end time must be a string"
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
