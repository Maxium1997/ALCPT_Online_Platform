from enum import Enum


class Gender(Enum):
    Unset = (0, 'Unset')
    Male = (1, 'Male')
    Female = (2, 'Female')
    Privacy = (3, 'Privacy')


class Identity(Enum):
    User = (1, 'User')
    Student = (2, 'Student')
    Teacher = (3, 'Teacher')


class Privilege(Enum):
    SystemManager = (0b100000, 'SystemManager')
    TestManager = (0b10000, 'TestManager')
    TBManager = (0b1000, 'TBManager')
    TBOperator = (0b100, 'TBOperator')
    Viewer = (0b10, 'Viewer')
    Testee = (0b1, 'Testee')
