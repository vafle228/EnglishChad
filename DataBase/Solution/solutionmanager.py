from typing import List

from ChadUtils.subscriber import ChadSubscriber, Subscriptions
from DataBase.Solution.solution import Solution
from DataBase.sqlmanager import ChadSqlManager


class SolutionManager:
    _database = ChadSqlManager.getInstance()

    @classmethod
    def initDatabase(cls) -> None:
        return cls._database.dataBaseInit('''
            CREATE TABLE ChadSolution (
                id SERIAL PRIMARY KEY,
                level TEXT NOT NULL,
                author TEXT NOT NULL,
                name TEXT NOT NULL UNIQUE,
                path TEXT NOT NULL UNIQUE)
        ''', 'ChadSolution')
    
    @classmethod
    def addSolution(cls, name: str, author: str, level: str, file_path: str) -> None:
        cls._database.addEntry(f'''
            INSERT INTO ChadSolution 
            (name, author, level, path) VALUES 
            ('{name}', '{author}', '{level}', '{file_path}')
        ''')
        
        ChadSubscriber.emitToSubscribers(Subscriptions.DATA_BASE_UPDATE)
        ChadSubscriber.emitToSubscribers(Subscriptions.SOLUTION_ADD, level, name)
    
    @classmethod
    def getSolutionByName(cls, solution_name: str) -> Solution:
        solution = cls._database.getEntries(f'''
            SELECT * FROM ChadSolution 
            WHERE name = '{solution_name}'
        ''')
        return Solution(*solution[0]) if solution else Solution()
    
    @classmethod
    def deleteSolutionByName(cls, solution_name: str) -> None:
        cls._database.deleteEntry(f'''
            DELETE FROM ChadSolution 
            WHERE name = '{solution_name}'
        ''')
        ChadSubscriber.emitToSubscribers(Subscriptions.DATA_BASE_UPDATE)
    
    @classmethod
    def getAllSolutions(cls) -> List[Solution]:
        get_command = "SELECT * FROM ChadSolution"
        return [Solution(*entry) for entry in cls._database.getEntries(get_command)]
