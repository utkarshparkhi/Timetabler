from course import Course
from room import Room
from faculty import Faculty
from timetabler import TimeTabler
from utils import generate_slots

# room = [[size,name]]
rooms = [[100, "LHC-001"],
         [40, "LHC-002"],
         [100, "LHC-003"],
         [100, "LHC-004"],
         [100, "LHC-005"]]

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
                ]

Faculties = []
for fac in faculty:
    Faculties.append(Faculty(fac[0], fac[1]))

slots = generate_slots()

Rooms = []
for room in rooms:
    Rooms.append(Room(room[0], room[1]))
# courses  = [[code, number_of_lectures, size, faculty, students, timing ,year ,type, slot, room]]
courses = [["ECN-212", 3, 50, ["VP"], [], "morning", 1, ['multiyear'], [slots[0]], Rooms[0]],
           ["ECN-205", 3, 50, ["SR"], [], "morning", 1, [], [], Rooms[2]]]
Courses = []
for course in courses:
    c = Course(course[0], course[1], course[2], course[3], course[4], course[5], course[6])
    for ty in course[7]:
        c.add_type(ty)
    for s in course[8]:
        c.add_slot(s)
    print(isinstance(course[9], Room), course[9] is not None)
    if course[9] is not None and isinstance(course[9], Room):
        print(course[9])
        c.add_room(course[9])
    Courses.append(c)

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
    if cs % 7 == 4:
        s.add_type('multiyear')
        print(s)
    t.add_slots(s)
    cs += 1

t.room_clash_constraint()
t.lecture_per_day_constraint()
t.course_clash_constraint()
t.course_room_assignment()
t.slot_assignment()
t.preference_constraint()
t.courses_in_same_type()
t.slots_enforced()
t.room_enforced()
r, m, rc2 = t.solve()
