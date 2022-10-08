import sqlite3 as sql


class ChadDataBaseManager:
    _chad_base = None

    def __new__(cls, *args, **kwargs):
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
                    path text NOT NULL UNIQUE)
            ''')
        except sql.OperationalError: pass
    

    def addEntry(self, name, file_path) -> None:
        self._database.execute(f'''
            INSERT INTO EnglishChad 
            (name, path) VALUES 
            ('{name}', '{file_path}')
        ''')
        self._connection.commit()
    

    def deleteEntryByName(self, entry_name) -> None:
        self._database.execute(f'''
            DELETE FROM EnglishChad 
            WHERE name = '{entry_name}'
        ''')
        self._connection.commit()
    

    def getEntriesByName(self, entry_name) -> list:
        return self._database.execute(f'''
            SELECT * FROM EnglishChad 
            WHERE name = '{entry_name}'
        ''').fetchall()
