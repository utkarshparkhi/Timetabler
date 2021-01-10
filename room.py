class Room:
    def __int__(self, size, name):
        assert isinstance(size, int), TypeError('size must be an integer')
        assert isinstance(name, str), TypeError('name must be an string')
        self.size = size
        self.name = name
