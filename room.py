class Room:
    def __init__(self, size, name):
        assert isinstance(size, int), "size must be an integer"
        assert isinstance(name, str), "name must be an string"
        self.size = size
        self.name = name
