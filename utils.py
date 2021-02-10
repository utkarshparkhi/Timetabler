from slot import Slot


def generate_slots():
    slots = []
    for day in range(1, 6):
        for start_time in range(1, 6):
            slots.append(Slot(day, start_time=start_time, end_time=start_time + 1))
        for start_time in range(7, 11):
            slots.append(Slot(day, start_time=start_time, end_time=start_time + 1))
    return slots


def generate_reverse_dictionary():
    reverse_dict = {}
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    time = ["8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM"]
    reverse_days = {}
    reverse_time = {}
    for i in range(len(days)):
        reverse_days[days[i]] = i + 1
    for i in range(len(time)):
        reverse_time[time[i]] = i + 1
    reverse_dict['days'] = reverse_days
    reverse_time['time'] = reverse_time
    return reverse_dict

