class Faculty: 
    def __init__(self, code, course, preference):
        assert isinstance(code, str), "ID of a faculty must be int"
        assert isinstance(course, list), "course must be a list of 'Course' instance"
        assert isinstance(preference, list), "preference must be a list of 'slot'"
