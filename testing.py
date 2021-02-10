from course import Course
from room import Room
from faculty import Faculty
from timetabler import TimeTabler
from utils import generate_slots, format_result

# courses  = [[code, number_of_lectures, size, faculty, students, timing ,year]]
courses = [["IPH-305", 2, 60, ["F1"], [], 'evening', 3],
            ["PHN-311", 6, 60, ["F2", "F1"], [], 'evening', 3],
            ["PHN-313", 6, 60, ["F3"], [], 'evening', 3],
            ["PHN-315", 3, 60, ["F4"], [], 'evening', 3],
            ["PHN-317", 2, 60, ["F4"], [], 'evening', 3],
            ["PHN-319", 3, 60, ["F5"], [], 'evening', 3],
            ["PHN-331", 3, 60, ["F6"], [], 'evening', 3]]

# room = [[size,name]]
rooms = [[100, "LHC-001"],
        [100, "LHC-002"],
        [100, "LHC-003"],
        [100, "LHC-004"],
        [100, "LHC-005"]]

# faculty = [[code]]
faculty = [["F1"],
           ["F2"],
           ["F3"],
           ["F4"],
           ["F5"],
           ["F6"]]

faculties = []
for fac in faculty:
    faculties.append(Faculty(fac[0]))

Rooms = []
for room in rooms:
    Rooms.append(Room(room[0], room[1]))

Courses = []
for course in courses:
    Courses.append(Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6]))

slots = generate_slots()
t = TimeTabler()
for c in Courses:
    t.add_course(c)
for r in Rooms:
    t.add_room(r)
cs = 0
for s in slots:
    t.add_slots(s)
    cs += 1
t.room_clash_constraint()
t.room_per_course_and_room_size_constraint()
t.assign_slots_constraint()
t.one_lec_in_one_day()
r, m, rc2 = t.solve()
