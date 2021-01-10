class Course:
    def __init__(self, code, number_of_lectures, size, faculty, timing):
        assert isinstance(code, str), "course code must be an string"
        assert isinstance(number_of_lectures, int), "number_of_lectures mus be an integer."
        assert isinstance(size, int), "size must be an integer"
        assert isinstance(faculty, list), "faculty must be an list of faculty codes"
        assert self.check_faculty_codes(faculty), "all faculty codes must be string"
        assert timing in ["morning", "evening"], "timing must be morning or evening"
        self.code = code
        self.number_of_lectures = number_of_lectures
        self.size = size
        self.faculty = faculty
        self.timing = timing

    def check_faculty_codes(self, faculty):
        for fac in faculty:
            if not isinstance(fac, str):
                return False
        return True
