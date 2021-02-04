class Student:
    def __init__(self, code, course):
        assert isinstance(code, int), "ID of a student must be int"
        assert isinstance(course, list), "course myst be a list of 'Course' instance" 