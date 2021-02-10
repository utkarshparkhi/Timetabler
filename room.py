class Room:
    def __init__(self, size, name):
        assert isinstance(size, int), "size must be an integer"
        assert isinstance(name, str), "name must be an string"
        self.size = size
        self.name = name

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return self.__str__()
