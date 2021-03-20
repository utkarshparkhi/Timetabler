from course import Course
from room import Room
from faculty import Faculty
from timetabler import TimeTabler
from utils import generate_slots, format_result

# courses  = [[code, number_of_lectures, number_of_practicals, size, faculty, students, timing ,year ,type, slot, room]]
courses = [["ECN-514", 3, 0, 50, ["AJ"], [], "morning", 1],
           ["ECN-611", 3, 0, 50, ["AS", "AKC"], [], "morning", 1],
           ["ECN-614", 3, 0, 50, ["SK"], [], "morning", 1],
           ["ECN-615", 3, 0, 50, ["AT"], [], "morning", 1],
           ["ECN-577", 3, 0, 50, ["AD"], [], "morning", 1],
           ["ECN-584", 3, 0, 50, ["SD"], [], "morning", 1],
           ["ECN-587", 3, 0, 50, ["VSP"], [], "morning", 1],
           ["ECN-591", 3, 0, 50, ["BKK"], [], "morning", 1],
           ["ECN-631", 3, 0, 50, ["NPP", "DB"], [], "morning", 1],
           ["ECN-534", 3, 0, 50, ["DS"], [], "morning", 1],
           ["ECN-550", 3, 0, 50, ["RKP"], [], "morning", 1],
           ["ECN-541", 3, 0, 50, ["AP"], [], "morning", 1],
           ["ECN-212", 3, 0, 50, ["VP"], [], "morning", 1],
           ["ECN-312", 3, 0, 50, ["PMP"], [], "evening", 1],
           ["ECN-316", 3, 0, 50, ["DK"], [], "evening", 1],
           ["ECN-102", 3, 1, 50, ["DG", "BS"], [], "morning", 1],
           ["ECN-104", 3, 0, 50, ["BPD", "BK"], [], "morning", 1],
           ["ECN-205", 3, 0, 50, ["SR"], [], "morning", 1],
           ["ECN-222", 3, 0, 50, ["AB"], [], "morning", 1],
           ["ECN-343", 3, 0, 50, ["SM"], [], "evening", 1],
           ["ECN-232", 3, 0, 50, ["DB", "NPP"], [], "morning", 1],
           ["ECN-342", 3, 0, 50, ["KR"], [], "evening", 1], ]

# room = [[size,name]]
rooms = [[100, "LHC-001"],
         [100, "LHC-002"],
         [100, "LHC-003"],
         [100, "LHC-004"],
         [100, "LHC-005"], 
         [100, "LHC-006"]]

# faculty = [[code,[preference]]
faculty = [["AJ", []],
           ["AS", []],
           ["AKC", []],
           ["SK", []],
           ["AT", []],
           ["AD", []],
           ["SD", []],
           ["VSP", []],
           ["BKK", []],
           ["NPP", []],
           ["DB", []],
           ["DS", []],
           ["RKP", []],
           ["AP", []],
           ["VP", []],
           ["PMP", []],
           ["DK", []],
           ["DG", []],
           ["BPD", []],
           ["BS", []],
           ["BK", []],
           ["SR", []],
           ["AB", []],
           ["SM", []],
           ["KR", []]]

# course_pairs = [[code, code]]
course_pairs = [["ECN-212", "ECN-205"],
                ["ECN-212", "ECN-222"],
                ["ECN-212", "ECN-232"],
                ["ECN-312", "ECN-316"],
                ["ECN-312", "ECN-343"],
                ["ECN-312", "ECN-342"],
                ["ECN-316", "ECN-343"],
                ["ECN-316", "ECN-342"],
                ["ECN-102", "ECN-104"],
                ["ECN-205", "ECN-222"],
                ["ECN-205", "ECN-232"],
                ["ECN-222", "ECN-232"],
                ["ECN-343", "ECN-342"],
                ["ECN-514", "ECN-577"],
                ["ECN-514", "ECN-584"],
                ["ECN-514", "ECN-587"],
                ["ECN-514", "ECN-591"],
                ["ECN-514", "ECN-534"],
                ["ECN-514", "ECN-550"],
                ["ECN-514", "ECN-541"],
                ["ECN-577", "ECN-584"],
                ["ECN-577", "ECN-587"],
                ["ECN-577", "ECN-591"],
                ["ECN-577", "ECN-534"],
                ["ECN-577", "ECN-550"],
                ["ECN-584", "ECN-587"],
                ["ECN-584", "ECN-591"],
                ["ECN-584", "ECN-534"],
                ["ECN-584", "ECN-550"],
                ["ECN-584", "ECN-541"],
                ["ECN-587", "ECN-591"],
                ["ECN-587", "ECN-534"],
                ["ECN-587", "ECN-550"],
                ["ECN-587", "ECN-541"],
                ["ECN-591", "ECN-534"],
                ["ECN-591", "ECN-550"],
                ["ECN-591", "ECN-541"],
                ["ECN-550", "ECN-541"],
                ["ECN-611", "ECN-614"],
                ["ECN-611", "ECN-615"],
                ["ECN-611", "ECN-631"],
                ["ECN-614", "ECN-615"],
                ["ECN-614", "ECN-631"],
                ["ECN-631", "ECN-615"],
                ['ECN-541', "ECN-534"]]

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
t.practical_per_day_constraint()
t.continuous_practical_assignment()
t.practical_slot_assignment()
t.preference_constraint()
r, m, rc2 = t.solve()