# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 09:54:09 2020

@author: parkh
"""
from course import Course
from pysat.formula import WCNFPlus
class TimeTabler:
    def __init__(self):
        self.courses = []
        self.CNF = WCNFPlus()
        self.slots = []
        self.rooms = []
        
    def add_course(self,course):
        if not isinstance(course, Course):
            raise TypeError("course must be an Course type")
        self.courses.append(course)
        return True
    
    def add
    