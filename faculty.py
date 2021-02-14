class Faculty: 
    def __init__(self, code, preference):
        assert isinstance(code, str), "ID of a faculty must be str"
        # assert isinstance(preference, list), "preference must be a list of 'Slot' instance"
        self.code = code
        self.preference = preference