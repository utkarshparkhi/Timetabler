from course import Course
from room import Room
from slot import Slot
from clause import Clause
from faculty import Faculty
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
        self.room_to_index = {}
        self.clauses = []
        self.clauses_converted = 0
        self.set1 = []
        self.slot_to_index = {}
        self.faculty_code_map = {}

    def add_course(self, course):
        assert isinstance(course, Course), "course must be an Course type"
        assert course.code not in self.courses_to_int.keys(), "course code already exist"
        self.courses_to_int[course.code] = len(self.courses)
        self.courses.append(course)
        return True

    def add_course_pair(self, course_pair):
        assert course_pair[0] in self.courses_to_int.keys(), "incorrect course code"
        assert course_pair[1] in self.courses_to_int.keys(), "incorrect course code"
        self.set1.append(course_pair)
        return True

    def add_faculty(self, faculty):
        assert isinstance(faculty, Faculty), "Faculty must be an Faculty type"
        self.faculties.append(faculty)
        self.faculty_code_map[faculty.code] = faculty.preference
        return True

    def add_room(self, room):
        assert isinstance(room, Room), TypeError("room must be a Room type")
        assert room.name not in self.room_to_index.keys(), "room already exists"
        self.room_to_index[room.name] = len(self.rooms)
        self.rooms.append(room)
        return True

    def add_slots(self, slot):
        assert isinstance(slot, Slot), "slot must be an slot type"
        self.slot_to_index[slot.day * 100 + slot.start_time] = len(self.slots)
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
                self.add_cnf(clause)
        self.clauses_converted = len(self.clauses)
        return True

    def add_cnf(self, clause):
        converted_clause = [self.convert_literal(literal) for literal in clause.literals]
        if clause.weight == -1:
            self.CNF.append(converted_clause)
            return True
        self.CNF.append(converted_clause, weight=clause.weight)
        return True

    def at_most(self, clause, k, at_least=False):
        for combination in combinations(clause.literals, k + 1):
            new_cls = Clause(-1)
            for lit in combination:
                new_lit = copy.deepcopy(lit)
                new_lit.Not ^= (True ^ at_least)
                new_cls.add_literal(new_lit)
            self.add_cnf(new_cls)

    def at_least(self, clause, k):
        n = len(clause.literals)
        self.at_most(clause, max(n - k, 0), at_least=True)

    def convert_literal(self, literal):
        if literal.Type == 1:
            return (((literal.course - 1) * len(self.slots)) + literal.room_slot) * (-1 if literal.Not else 1)
        else:
            return ((len(self.courses) * len(self.slots)) + (
                    ((literal.course - 1) * len(self.rooms)) + literal.room_slot)) * (
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

    def course_room_assignment(self):
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

    def slot_assignment(self):
        """
        Morning slots before 2 and Evening after 2
        and
        Number of slots assigned == c.no_of_lectures
        :return:
        """

        for c in range(len(self.courses)):
            clause = Clause(-1, at_most=self.courses[c].number_of_lectures,
                            at_least=self.courses[c].number_of_lectures)
            for s in range(len(self.slots)):
                if self.courses[c].timing == "morning" and self.slots[s].start_time <= 5:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
                elif self.courses[c].timing == "evening" and self.slots[s].start_time > 6:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
            self.add_clause(clause)

    def practical_slot_assignment(self):
        """
        Morning slots before 2 and Evening after 2
        and
        Number of slots assigned == c.no_of_practicals
        :return:
        """

        for c in range(len(self.courses)):
            clause = Clause(-1, at_most=self.courses[c].number_of_practicals*2,
                            at_least=self.courses[c].number_of_practicals*2)
            for s in range(len(self.slots)):
                if self.courses[c].timing == "morning" and self.slots[s].start_time>6:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
                elif self.courses[c].timing == "evening" and self.slots[s].start_time <= 5:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
            self.add_clause(clause)

    def course_clash_constraint(self):
        """
        ~Cc1Ss | ~Cc2Ss
        :return:
        """

        for c in self.set1:
            for s in range(len(self.slots)):
                clause = Clause(-1)
                clause.add_literal(Literal(1, self.courses_to_int[c[0]] + 1, s + 1, True))
                clause.add_literal(Literal(1, self.courses_to_int[c[1]] + 1, s + 1, True))
                self.add_clause(clause)

    def preference_constraint(self):
        """
        CcSs
        :return:
        """
        for c in self.courses:
            for f in c.faculty:
                for s in self.faculty_code_map[f]:
                    var = s[0] * 100 + s[1]
                    clause = Clause(1)
                    clause.add_literal(Literal(1, self.courses_to_int[c.code] + 1, self.slot_to_index[var] + 1, False))
                    self.add_clause(clause)

    def lecture_per_day_constraint(self):
        """
        atmost 1 of all CcSs (s belongs to a particular day)
        :return:
        """

        for c in range(len(self.courses)):
            for d in range(1, 6):
                clause = Clause(-1, at_most=1)
                for s in range(len(self.slots)):
                    if(self.slots[s].day==d):
                        if self.courses[c].timing == "morning" and self.slots[s].start_time <= 5:
                            clause.add_literal(Literal(1, c + 1, s + 1, False))
                        elif self.courses[c].timing == "evening" and self.slots[s].start_time > 6:
                            clause.add_literal(Literal(1, c + 1, s + 1, False))
                self.add_clause(clause)

    def practical_per_day_constraint(self):
        """
        atmost 2 of all CcSs (s belongs to a particular day)
        :return:
        """

        for c in range(len(self.courses)):
            for d in range(1, 6):
                clause = Clause(-1, at_most=2*self.courses[c].number_of_practicals)
                for s in range(len(self.slots)):
                    if(self.slots[s].day==d):
                        if self.courses[c].timing == "morning" and self.slots[s].start_time > 6:
                            clause.add_literal(Literal(1, c + 1, s + 1, False))
                        elif self.courses[c].timing == "evening" and self.slots[s].start_time <= 5:
                            clause.add_literal(Literal(1, c + 1, s + 1, False))
                self.add_clause(clause)
        
        # not working else working
        # for c in range(len(self.courses)):
        #     for d in range(1, 6):
        #         clause = Clause(1, at_least=2*self.courses[c].number_of_practicals)
        #         for s in range(len(self.slots)):
        #             if(self.slots[s].day==d):
        #                 if self.courses[c].timing == "morning" and self.slots[s].start_time > 6:
        #                     clause.add_literal(Literal(1, c + 1, s + 1, False))
        #                 elif self.courses[c].timing == "evening" and self.slots[s].start_time <= 5:
        #                     clause.add_literal(Literal(1, c + 1, s + 1, False))
        #         self.add_clause(clause)

    def continuous_practical_assignment(self):
        """
        atmost 2 of all CcSs (s belongs to a particular day)
        :return:
        """

        for c in range(len(self.courses)):
            for d in range(1, 6):
                for s in range(len(self.slots)):
                    clause = Clause(-1)
                    if(self.slots[s].day==d):
                        if self.courses[c].timing == "morning" and self.slots[s].start_time==7:
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 1, True))
                            clause.add_literal(Literal(1, c + 1, s + 3, True))
                            self.add_clause(clause)
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 2, True))
                            clause.add_literal(Literal(1, c + 1, s + 4, True))
                            self.add_clause(clause)
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 1, True))
                            clause.add_literal(Literal(1, c + 1, s + 4, True))
                            self.add_clause(clause)
                        elif self.courses[c].timing == "evening" and self.slots[s].start_time==1:
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 1, True))
                            clause.add_literal(Literal(1, c + 1, s + 3, True))
                            self.add_clause(clause)
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 2, True))
                            clause.add_literal(Literal(1, c + 1, s + 4, True))
                            self.add_clause(clause)
                            clause = Clause(-1)
                            clause.add_literal(Literal(1, c + 1, s + 1, True))
                            clause.add_literal(Literal(1, c + 1, s + 4, True))
                            self.add_clause(clause)

    def courses_in_same_type(self):
        for c in range(len(self.courses)):
            for s in range(len(self.slots)):
                co = self.courses[c]
                sl = self.slots[s]
                if co.type.intersection(sl.type) != co.type:
                    clause = Clause(1000)
                    clause.add_literal(Literal(1, c + 1, s + 1, True))
                    self.add_clause(clause)

    def slots_enforced(self):
        for c in range(len(self.courses)):
            for sl in self.courses[c].slots:
                clause = Clause(-1)
                s = self.slot_to_index[sl.day * 100 + sl.start_time]
                clause.add_literal(Literal(1, c + 1, s + 1, False))
                self.add_clause(clause)

    def room_enforced(self):
        for c in range(len(self.courses)):
            if self.courses[c].room_assigned():
                if self.courses[c].room.name in self.room_to_index.keys():
                    r = self.room_to_index[self.courses[c].room.name]
                    clause = Clause(-1)
                    clause.add_literal(Literal(2, c + 1, r + 1, False))
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
        if model is None:
            print("All hard clauses not satisfied")
            return None
        result = {}
        for c in range(len(self.courses)):
            slots = []
            for s in range(len(self.slots)):
                pos = self.convert_literal(Literal(1, c + 1, s + 1, False))
                if len(model) >= pos:
                    if model[pos - 1] > 0:
                        slots.append(self.slots[s])
            room = []
            for r in range(len(self.rooms)):
                pos = self.convert_literal(Literal(2, c + 1, r + 1, False))
                if len(model) >= pos:
                    if model[pos - 1] > 0:
                        room.append(self.rooms[r])
            result[self.courses[c].code] = {"slots": slots, "room": room}
        return result, model, rc2
