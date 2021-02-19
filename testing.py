from course import Course
from room import Room
from faculty import Faculty
from timetabler import TimeTabler
from utils import generate_slots, format_result

# courses  = [[code, number_of_lectures, size, faculty, students, timing ,year]]
courses = [["IPH-305", 2, 60, ["F1"], [], 'evening', 3],
           ["PHN-311", 3, 60, ["F2", "F1"], [], 'evening', 3],
           ["PHN-313", 3, 60, ["F3"], [], 'evening', 3],
           ["PHN-315", 3, 60, ["F4"], [], 'evening', 3],
           ["PHN-317", 2, 60, ["F4"], [], 'evening', 3],
           ["PHN-319", 3, 60, ["F5"], [], 'evening', 3],
           ["PHN-331", 3, 60, ["F6"], [], 'evening', 3]]

# room = [[size,name]]
rooms = [[100, "LHC-001"],
         [40, "LHC-002"],
         [100, "LHC-003"],
         [100, "LHC-004"],
         [100, "LHC-005"]]

# faculty = [[code,[preference]]
faculty = [["F1", [[1, 7, 8], [2, 7, 8], [3, 7, 8], [4, 7, 8], [5, 7, 8]]],
           ["F2", []],
           ["F3", []],
           ["F4", []],
           ["F5", []],
           ["F6", []]]

# course_pairs = [[code, code]]
course_pairs = [["IPH-305", "PHN-311"],
                ["IPH-305", "PHN-313"],
                ["IPH-305", "PHN-315"],
                ["IPH-305", "PHN-317"],
                ["PHN-311", "PHN-313"],
                ["PHN-311", "PHN-315"],
                ["PHN-311", "PHN-317"],
                ["PHN-313", "PHN-315"],
                ["PHN-313", "PHN-317"],
                ["PHN-315", "PHN-317"]]

Faculties = []
for fac in faculty:
    Faculties.append(Faculty(fac[0], fac[1]))

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
for f in Faculties:
    t.add_faculty(f)
for cp in course_pairs:
    t.add_course_pair(cp)
cs = 0
for s in slots:
    t.add_slots(s)
    cs += 1

t.room_clash_constraint()
t.lecture_per_day_constraint()
t.course_clash_constraint()
t.course_room_assignment()
t.slot_assignment()
t.preference_constraint()
r, m, rc2 = t.solve()
