from literal import Literal


class Clause:
    def __init__(self, weight):
        assert isinstance(weight, int) and weight >= -1, "weight must be an integer greater than aur equal to -1"
        self.weight = weight
        self.literals = []

    def add_literal(self, literal):
        assert isinstance(literal, Literal), "literal must be an literal instance"
        self.literals.append(literal)
