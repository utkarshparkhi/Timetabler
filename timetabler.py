from course import Course
from room import Room
from slot import Slot
from clause import Clause
from clause import Clause
from literal import Literal
from pysat.formula import WCNF
from pysat.examples.rc2 import RC2
from pysat.solvers import Solver
from itertools import combinations
import copy


class TimeTabler:
    """
    1 ... c*s
    c*s + (1 ... c.r)
    """

    def __init__(self):
        self.courses = []
        self.courses_to_int = {}
        self.CNF = WCNF()
        self.slots = []
        self.faculties = []
        self.students = []
        self.rooms = []
        self.room_to_int = {}
        self.clauses = []
        self.clauses_converted = 0
        self.set1 = {}

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
        assert isinstance(clause, Clause), "Clause must be an Clause type"

        self.clauses.append(clause)
        return True

    def generate_cnf(self):
        if len(self.clauses) <= self.clauses_converted:
            return True
        temp = self.clauses_converted
        for i in range(temp, len(self.clauses)):
            clause = self.clauses[i]
            if clause.at_most is not None:
                self.at_most(clause, clause.at_most)
            if clause.at_least is not None:
                self.at_least(clause, clause.at_least)
            if clause.at_most is None and clause.at_least is None:
                self.add_CNF(clause)
        self.clauses_converted = len(self.clauses)
        return True

    def add_CNF(self, clause):
        converted_clause = [self.convert_literal(literal) for literal in clause.literals]
        self.CNF.append(converted_clause, weight=clause.weight)
        return True

    def at_most(self, clause, k, at_least=False):
        for combination in combinations(clause.literals, k + 1):
            new_cls = Clause(-1)
            for lit in combination:
                new_lit = copy.deepcopy(lit)
                new_lit.Not ^= (True ^ at_least)
                new_cls.add_literal(new_lit)
            self.add_CNF(new_cls)

    def at_least(self, clause, k):
        n = len(clause.literals)
        print(n,k)
        self.at_most(clause, max(n - k, 0), at_least=True)

    def convert_literal(self, literal):
        if literal.Type == 1:
            return (((literal.course-1) * len(self.slots)) + literal.room_slot) * (-1 if literal.Not else 1)
        else:
            return ((len(self.courses) * len(self.slots)) + (
                    ((literal.course-1) * len(self.rooms)) + literal.room_slot)) * (
                       -1 if literal.Not else 1)

    def room_clash_constraint(self):
        """
        ~Cc1Ss | ~Cc2Ss | ~Cc1Rr | ~Cc2Rr
        :return:
        """

        for c1 in range(len(self.courses)):
            for c2 in range(len(self.courses)):
                if c1 != c2:
                    for s in range(len(self.slots)):
                        for r in range(len(self.rooms)):
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c1 + 1, s + 1, True))
                            clause.add_literal(Literal(1, c2 + 1, s + 1, True))
                            clause.add_literal(Literal(2, c1 + 1, r + 1, True))
                            clause.add_literal(Literal(2, c2 + 1, r + 1, True))
                            self.add_clause(clause)

    def room_per_course_and_room_size_constraint(self):
        """
        exactly one(CcRr) given r.size >= c.size
        and
        ~CcRr given r.size < c.size
        :return:
        """

        for c in range(len(self.courses)):
            clause = Clause(-1, at_most=1, at_least=1)
            for r in range(len(self.rooms)):
                if self.courses[c].size <= self.rooms[r].size:
                    clause.add_literal(Literal(2, c + 1, r + 1, False))
                elif self.courses[c].size > self.rooms[r].size:
                    clause2 = Clause(-1)
                    clause2.add_literal(Literal(2, c + 1, r + 1, True))
                    self.add_clause(clause2)
            # exactly one of all these literals true
            self.add_clause(clause)

    def assign_slots_constraint(self):
        """
        Morning slots before 2 and Evening after 2
        and
        Number of slots assigned == c.no_of_lectures
        :return:
        """

        for c in range(len(self.courses)):
            clause = Clause(-1, at_most=self.courses[c].number_of_lectures, at_least=self.courses[c].number_of_lectures)
            for s in range(len(self.slots)):
                if self.courses[c].timing == "morning" and self.slots[s].start_time < 5:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
                elif self.courses[c].timing == "evening" and self.slots[s].start_time >= 5:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
            self.add_clause(clause)

    def fac_stu_course_clash_constraint(self):
        """
        ~Cc1Ss | ~Cc2Ss
        :return:
        """

        for c in self.set1:
            if (c[0] != c[1]):
                for s in range(len(self.slots)):
                    clause = Clause(-1)
                    clause.add_literal(Literal(1, c[0], s, True))
                    clause.add_literal(Literal(1, c[1], s, True))
                    self.add_clause(clause)

    def prof_prefernce_constraint(self):
        """
        CcSs
        :return:
        """

        for f in self.faculties:
            for c in f.courses:
                for s in f.prefernce:
                    clause = Clause(500)
                    clause.add_literal(Literal(1, c, s, False))
                    self.add_clause(clause)

    def one_lec_in_one_day(self):
        """
        atmost 1 of all CcSs (s belongs to a particular day)
        :return:
        """

        for c in range(len(self.courses)):
            for d in range(1, 6):
                clause = Clause(-1, at_most=1)
                for s in range(len(self.slots)):
                    if self.slots[s].day == d:
                        clause.add_literal(Literal(1, c+1, s+1, False))
                self.add_clause(clause)

    def solve(self):
        print("generating formula")
        self.generate_cnf()
        print("formula generated")
        # result =  {course:{slots:[],room:[]}}
        rc2 = RC2(self.CNF)
        print("solving MAXSAT")
        model = rc2.compute()
        print("MAXSAT solved")
        result = {}
        for c in range(len(self.courses)):
            slots = []
            for s in range(len(self.slots)):
                pos = self.convert_literal(Literal(1, c + 1, s + 1, False))
                if len(model) >= pos:
                    if model[pos-1] > 0:
                        slots.append(self.slots[s])
            room = []
            for r in range(len(self.rooms)):
                pos = self.convert_literal(Literal(2, c + 1, r + 1, False))
                if len(model) >= pos:
                    if model[pos-1] > 0:
                        room.append(self.rooms[r])
            result[self.courses[c].code] = {"slots": slots, "room": room}
        return result, model, rc2
