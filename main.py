import sqlite3 as sql
from typing_extensions import Self


class ChadDataBase:
    _chad_base = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._chad_base is None:
            cls._chad_base = super().__new__(cls, *args, **kwargs)
        return cls._chad_base

    def __init__(self) -> None:
        self._connection = sql.connect('db.sqlite3')
        self._database = self._connection.cursor()

        try:
            self._database.execute('''
                CREATE TABLE EnglishChad (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL, 
                    path text NOT NULL UNIQUE
                )
            ''')
        except sql.OperationalError:
            pass
    

    def addFile(self, name, file):
        pass

