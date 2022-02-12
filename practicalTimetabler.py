from clause import Clause
from literal import Literal
from timetabler import TimeTabler


class PracticalTimetabler(TimeTabler):

    def practical_slot_assignment(self):
        """
        Morning slots before 2 and Evening after 2
        and
        Number of slots assigned == c.no_of_practicals
        :return:
        """

        for c in range(len(self.courses)):
            clause = Clause(-1, at_most=self.courses[c].number_of_practicals * 2,
                            at_least=self.courses[c].number_of_practicals * 2)
            for s in range(len(self.slots)):
                if self.courses[c].timing == "morning" and self.slots[s].start_time > 6:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
                elif self.courses[c].timing == "evening" and self.slots[s].start_time <= 5:
                    clause.add_literal(Literal(1, c + 1, s + 1, False))
            self.add_clause(clause)

    def practical_per_day_constraint(self):
        """
        atmost 2 of all CcSs (s belongs to a particular day)
        :return:
        """

        for c in range(len(self.courses)):
            for d in range(1, 6):
                clause = Clause(-1, at_most=2 * self.courses[c].number_of_practicals)
                for s in range(len(self.slots)):
                    if(self.slots[s].day == d):
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
                    if(self.slots[s].day == d):
                        if self.courses[c].timing == "morning" and self.slots[s].start_time == 7:
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
                        elif self.courses[c].timing == "evening" and self.slots[s].start_time == 1:
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
