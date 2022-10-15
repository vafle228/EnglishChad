from enum import Enum
from typing import List

from ChadUtils.subscriber import ChadSubscriber, Subscriptions
from DataBase.sqlmanager import ChadSqlManager


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


class SolutionManager:
    _database = ChadSqlManager.getInstance()

    @classmethod
    def initDatabase(cls) -> None:
        return cls._database.dataBaseInit('''
            CREATE TABLE EnglishChad (
                id SERIAL PRIMARY KEY,
                level TEXT NOT NULL,
                author TEXT NOT NULL,
                name TEXT NOT NULL UNIQUE,
                path TEXT NOT NULL UNIQUE)
        ''', 'EnglishChad')
    
    @classmethod
    def addSolution(cls, name: str, author: str, level: str, file_path: str) -> None:
        cls._database.addEntry(f'''
            INSERT INTO EnglishChad 
            (name, author, level, path) VALUES 
            ('{name}', '{author}', '{level}', '{file_path}')
        ''')
        ChadSubscriber.emitToSubscribers(Subscriptions.DATA_BASE_UPDATE)
    
    @classmethod
    def getSolutionByName(cls, solution_name: str) -> Solution:
        solution = cls._database.getEntries(f'''
            SELECT * FROM EnglishChad 
            WHERE name = '{solution_name}'
        ''')
        return Solution(*solution[0]) if solution else Solution()
    
    @classmethod
    def deleteSolutionByName(cls, solution_name: str) -> None:
        cls._database.deleteEntry(f'''
            DELETE FROM EnglishChad 
            WHERE name = '{solution_name}'
        ''')
        ChadSubscriber.emitToSubscribers(Subscriptions.DATA_BASE_UPDATE)
    
    @classmethod
    def getAllSolutions(cls) -> List[Solution]:
        get_command = "SELECT * FROM EnglishChad"
        return [Solution(*entry) for entry in cls._database.getEntries(get_command)]
