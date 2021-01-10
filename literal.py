class Literal:
    def __init__(self, _type, course, room_slot, _not):
        assert type in [1, 2], "type must be 1 or 2"
        assert isinstance(course, int), "course must be an int"
        assert isinstance(room_slot, int), "room or slot must be an int"
        assert isinstance(_not, bool), "_not must be an boolean"
        self.Type = _type
        self.course = course
        self.room_slot = room_slot
        self.Not = _not
