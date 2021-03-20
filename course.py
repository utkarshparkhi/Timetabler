from room import Room
from slot import Slot


class Course:
    def __init__(self, code, number_of_lectures, number_of_practicals, size, faculty, student, timing):
        assert isinstance(code, str), "course code must be an string"
        assert isinstance(number_of_lectures, int), "number_of_lectures must be an integer."
        assert isinstance(number_of_practicals, int), "number_of_practicals must be an integer."
        assert isinstance(size, int), "size must be an integer"
        assert isinstance(student, list), "student must be a list of 'Student' instance"
        assert isinstance(faculty, list), "faculty must be a list of 'Faculty' instance"
        # assert isinstance(year, int), "Year should be an integer value"
        assert self.check_faculty_codes(faculty), "all faculty codes must be string"
        assert self.check_student_codes(student), "all student codes must be int"
        assert timing in ["morning", "evening"], "timing must be morning or evening"
        self.code = code
        self.number_of_lectures = number_of_lectures
        self.number_of_practicals = number_of_practicals
        self.size = size
        self.faculty = faculty
        self.student = student
        self.timing = timing
        self.type = set()
        self.slots = []
        self.room = None

    def check_faculty_codes(self, faculty):
        for fac in faculty:
            if not isinstance(fac, str):
                return False
        return True

    def check_student_codes(self, student):
        for stu in student:
            if not isinstance(stu, int):
                return False
        return True

    def add_type(self, type):
        assert isinstance(type, str)
        self.type.add(type)
        return True

    def add_slot(self, slot):
        assert isinstance(slot, Slot)
        if len(self.slots) == self.number_of_lectures + self.number_of_practicals*2:
            raise Exception("All lectures have been assigned a slot")
        self.slots.append(slot)

    def add_room(self, room):
        assert isinstance(room, Room)
        self.room = room

    def room_assigned(self):
        return self.room is not None
