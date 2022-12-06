from typing import List

from DataBase.sqlmanager import ChadSqlManager
from DataBase.Subscribe.subscribe import Subscribe


class SubscribeManager:
    _database = ChadSqlManager.getInstance()

    @classmethod
    def initDatabase(cls) -> None:
        return cls._database.dataBaseInit('''
            CREATE TABLE ChadSubscribe (
                id SERIAL PRIMARY KEY,
                level TEXT NOT NULL,
                chatid INTEGER NOT NULL)
            ''')
    
    @classmethod
    def addSubscribe(cls, level: str, chatid: int) -> None:
        return cls._database.addEntry(f'''
            INSERT INTO ChadSubscribe 
            (level, chatid) VALUES 
            ('{level}', {chatid})
        ''')
    
    @classmethod
    def deleteSubscribeById(cls, id: int) -> None:
        return cls._database.deleteEntry(f'''
            DELETE FROM ChadSubscribe WHERE id = {id}
        ''')
    
    @classmethod
    def getSubscribe(cls, level: str, chatid: int) -> Subscribe:
        subscribe = cls._database.getEntries(f'''
            SELECT * FROM ChadSubscribe WHERE 
            level = '{level}' AND chatid = {chatid}
        ''')
        return Subscribe(*subscribe[0]) if subscribe else Subscribe()
    
    @classmethod
    def getSubscribesByLevel(cls, level: str) -> List[Subscribe]:
        get_command = f"SELECT * FROM ChadSubscribe WHERE level = '{level}'"
        return [Subscribe(*entry) for entry in cls._database.getEntries(get_command)]
    
    @classmethod
    def getAllSubscribes(cls) -> List[Subscribe]:
        get_command = "SELECT * FROM ChadSubscribe"
        return [Subscribe(*entry) for entry in cls._database.getEntries(get_command)]
