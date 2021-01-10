from course import Course
from room import Room
from slot import Slot
from clause import Clause
from literal import Literal
from pysat.formula import WCNFPlus


class TimeTabler:
    """
    1 ... c*s
    c*s + (1 ... c.f)
    """

    def __init__(self):
        self.courses = []
        self.courses_to_int = {}
        self.CNF = WCNFPlus()
        self.slots = []
        self.rooms = []
        self.room_to_int = {}
        self.clauses = []
        self.clauses_converted = 0

    def add_course(self, course):
        assert isinstance(course, Course), "course must be an Course type"
        assert course.code not in self.courses_to_int.keys(), "course code already exist"
        self.courses_to_int[course.code] = len(self.courses)
        self.courses.append(course)
        return True

    def add_room(self, room):
        assert isinstance(room, Room), TypeError("room must be a Room type")
        assert room.name not in self.room_to_int.keys(), "room already exists"
        self.room_to_int[room.name] = len(self.rooms)
        self.rooms.append(room)
        return True

    def add_slots(self, slot):
        assert isinstance(slot, Slot), "slot must be an slot type"
        self.slots.append(slot)
        return True

    def add_clause(self, clause):
        assert isinstance(clause, Clause), "Clause must be an list type"
        self.clauses.append(clause)
        return True

    def generate_cnf(self):
        if len(self.clauses) <= self.clauses_converted:
            return True
        temp = self.clauses_converted
        for i in range(temp, len(self.clauses)):
            clause = self.clauses[i]
            converted_clause = [self.convert_literal(literal) for literal in clause.literals]
            self.CNF.append(converted_clause, weight=clause.weight)
        return True

    def convert_literal(self, literal):
        if literal.Type == 1:
            return literal.course * literal.room_slot * (-1 if literal.Not else 1)
        else:
            return ((len(self.courses) * len(self.rooms)) + (literal.course * literal.room_slot)) * (
                -1 if literal.Not else 1)

    def room_clashes_constraint(self):
        """
        ~Cc1Ss | ~Cc2Ss | ~Cc1Rr | ~Cc2
        :return:
        """

        for c1 in range(len(self.courses)):
            for c2 in range(len(self.courses)):
                for s in range(len(self.slots)):
                    for r in range(len(self.rooms)):
                        clause = Clause(-1)
                        clause.add_literal(Literal(1, c1, s, True))
                        clause.add_literal(Literal(1, c2, s, True))
                        clause.add_literal(Literal(2, c1, r, True))
                        clause.add_literal(Literal(2, c2, r, True))
                        self.add_clause(clause)
