from typing import List
import sqlite3

from ChadUtils.constants import DB_LOCATION


class ChadSqlManager:
    _chad_base = None

    def __init__(self) -> None:
        self._connection = sqlite3.connect(DB_LOCATION)
        self._cursor = self._connection.cursor()
    
    @staticmethod
    def getInstance():
        if ChadSqlManager._chad_base is None:
            ChadSqlManager._chad_base = ChadSqlManager() 
        return ChadSqlManager._chad_base
    
    def dataBaseInit(self, init_command: str) -> None:
        try:
            self._cursor.execute(init_command)
            self._connection.commit()
        except sqlite3.OperationalError: return

    def addEntry(self, insert_command: str) -> None:
        self._cursor.execute(insert_command); self._connection.commit()

    def deleteEntry(self, delete_command: str) -> None:
        self._cursor.execute(delete_command); self._connection.commit()

    def getEntries(self, search_command: str) -> List[tuple]:
        self._cursor.execute(search_command); return self._cursor.fetchall()
