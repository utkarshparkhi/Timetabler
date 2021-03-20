# class Slot_2:
#     """
#     day
#     1 = monday
#     2 = tuesday
#     3 = wednesday
#     4 = thursday
#     5 = friday
#     6 = saturday
#     7 = sunday
#     --------------
#     time
#     1 = 9AM-11AM
#     2 = 10AM-12AM
#     3 = 11AM-1PM
#     4 = 2PM-4PM
#     5 = 3PM-5PM
#     6 = 4PM-6PM
#     """

#     def __init__(self, day, start_time):
#         assert isinstance(day, int), "day must be a int"
#         assert isinstance(start_time, int), "start time must be a int"
#         # assert isinstance(end_time, int), "end time must be a int"
#         self.day = day
#         self.start_time = start_time
#         # self.end_time = end_time
#         self.type = set()

#     def __repr__(self):
#         days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
#         time = ["9AM-11AM", "10AM-12AM", "11AM-1PM", "2PM-4PM", "3PM-5PM", "4PM-6PM"]
#         return f'{days[self.day - 1]} {time[self.start_time - 1]}'

#     def add_type(self, type):
#         assert isinstance(type, str)
#         self.type.add(type)
#         return True