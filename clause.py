from literal import Literal


class Clause:
    def __init__(self, weight, **kwargs):
        assert isinstance(weight, int) and weight >= -1, "weight must be an integer greater than aur equal to -1"
        self.weight = weight
        self.at_most = None if "at_most" not in kwargs.keys() else kwargs["at_most"]
        self.at_least = None if "at_least" not in kwargs.keys() else kwargs["at_least"]
        self.literals = []

    def add_literal(self, literal):
        assert isinstance(literal, Literal), "literal must be an literal instance"
        self.literals.append(literal)

    def __str__(self):
        ret = "["
        for lit in self.literals:
            ret+=f" {lit.__str__()},"
        ret+="]"
        return ret

    def __repr__(self):
        return self.__str__()
