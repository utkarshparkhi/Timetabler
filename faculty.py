class Faculty: 
    def __init__(self, code, course):
        assert isinstance(code, str), "ID of a faculty must be int"
        assert isinstance(course, list), "course myst be a list of 'Course' instance"
