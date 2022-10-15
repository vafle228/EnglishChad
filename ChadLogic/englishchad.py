from io import BufferedReader
from typing import Union

from MessageStructs.basestruct import IMessage

from ChadLogic.addentry import AddEntryMixin
from ChadLogic.delentry import DeleteEntryMixin
from ChadLogic.getentry import GetEntryMixin
from ChadLogic.helpmsg import HelpMessageMixin
from ChadLogic.replies import HELP_MSG
from ChadLogic.showentries import ShowAllEntriesMixin


class EnglishChadBot(
    AddEntryMixin, 
    DeleteEntryMixin, 
    GetEntryMixin, 
    ShowAllEntriesMixin, 
    HelpMessageMixin
):
    _handle_users = dict()

    @classmethod
    def startUserHandling(cls, message: IMessage, command: str) -> None:
        cls._handle_users[message.username] = {
            "/help": [cls.sendHelpMessage],
            "/start": [cls.sendHelpMessage],
            "/delSolution": [cls.startDelCommand ,cls.delEntry],
            "/getSolution": [cls.startGetCommand, cls.getEntry],
            "/showSolution": [cls.startShowCommand, cls.showEntriesList],
            "/addSolution": [
                cls.startAddCommand, 
                cls.getEntryName, 
                cls.getEntryLevel,
                cls.getEntryFile
            ],
        }[command]
    
    @classmethod
    def handleUserMessage(cls, message: IMessage) -> Union[str, BufferedReader]:
        if message.username not in cls._handle_users.keys():
            return HELP_MSG
        
        is_success, result = cls._handle_users[message.username][0](message)
        cls._cleanSubscribers(message.username, is_success)
        
        return result
    
    @classmethod
    def _cleanSubscribers(cls, username: str, is_success: bool) -> None:
        if is_success:
            cls._handle_users[username].pop(0)
        
        if len(cls._handle_users[username]) == 0:
            cls._handle_users.pop(username)
