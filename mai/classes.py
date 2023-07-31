from typing import List
from dataclasses import dataclass


@dataclass
class Student:
    snils: str
    points: int
    podl: bool
    priority: int


@dataclass
class UniversityDirection:
    name: str
    places: int
    students: List[Student]

    def add(self, s: Student):
        if len(self.students) < self.places:
            self.students.append(s)
            return True
        else:
            return False

    def get_min_points(self):
        if len(self.students) > 0:
            return min([x.points for x in self.students])
        else:
            return -1


@dataclass
class UniversityDirection2:
    link: str
    name: str
    place: str
    level: str
    pay: str
    form: str
    places: int
    students: List[Student]

    def add(self, s: Student):
        if len(self.students) < self.places:
            self.students.append(s)
            return True
        else:
            return False

    def get_min_points(self):
        if len(self.students) > 0:
            return min([x.points for x in self.students])
        else:
            return -1
