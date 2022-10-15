from enum import Enum


class SolutionLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"

    @classmethod
    def hasValue(cls, value):
        return value in cls._value2member_map_ 


class Solution:
    id: int = None
    level: str = None
    author: str = None
    name: str = None
    path: str = None

    def __init__(self, *args):
        attrs = ["id", "level", "author", "name", "path"]
        for i in range(min(len(args), len(attrs))):
            setattr(self, attrs[i], args[i])
