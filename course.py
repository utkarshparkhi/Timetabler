from room import Room


class Course:
    def __init__(self, code, number_of_lectures, size, faculty, student, timing,  year):
        assert isinstance(code, str), "course code must be an string"
        assert isinstance(number_of_lectures, int), "number_of_lectures mus be an integer."
        assert isinstance(size, int), "size must be an integer"
        assert isinstance(student, list), "student must be a list of 'Student' instance"
        assert isinstance(faculty, list), "faculty must be a list of 'Faculty' instance"
        assert isinstance(year, int), "Year should be an integer value"
        assert self.check_faculty_codes(faculty), "all faculty codes must be string"
        assert self.check_student_codes(student), "all student codes must be int"
        assert timing in ["morning", "evening"], "timing must be morning or evening"
        self.code = code
        self.number_of_lectures = number_of_lectures
        self.size = size
        self.faculty = faculty
        self.student = student
        self.timing = timing

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
