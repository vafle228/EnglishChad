from typing import List

import psycopg2
from ChadUtils.constants import DB_NAME, HOST, PASSWORD, USER


class ChadSqlManager:
    _chad_base = None

    def __init__(self) -> None:
        self._connection = psycopg2.connect(
            host=HOST, user=USER, 
            password=PASSWORD, database=DB_NAME
        )
    
    @staticmethod
    def getInstance():
        if ChadSqlManager._chad_base is None:
            ChadSqlManager._chad_base = ChadSqlManager() 
        return ChadSqlManager._chad_base
    
    def dataBaseInit(self, init_command: str, table_name: str) -> None:
        if self.tableExists(table_name):
            return
        
        with self._connection.cursor() as cursor:
            cursor.execute(init_command)
            self._connection.commit()
    
    def tableExists(self, table_name: str) -> bool:
        with self._connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT EXISTS(SELECT 1 FROM information_schema.tables 
                    WHERE table_catalog='{DB_NAME}' AND 
                    table_schema='public' AND
                    table_name='{table_name.lower()}')
            ''')
            return cursor.fetchone()[0]

    def addEntry(self, insert_command) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(insert_command)
            self._connection.commit()

    def deleteEntry(self, delete_command) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(delete_command)
            self._connection.commit()

    def getEntries(self, search_command: str) -> List[tuple]:
        with self._connection.cursor() as cursor:
            cursor.execute(search_command)
            return cursor.fetchall()
