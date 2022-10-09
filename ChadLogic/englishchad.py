from ChadLogic.addentry import AddEntryMixin
from ChadLogic.delentry import DeleteEntryMixin
from ChadLogic.getentry import GetEntryMixin

from telebot.types import Message
from ChadLogic.replies import HELP_MSG
from typing import Union
from io import BufferedReader


class EnglishChadBot(AddEntryMixin, DeleteEntryMixin, GetEntryMixin):
    _handle_users = dict()

    @classmethod
    def startUserHandling(cls, message: Message, command: str) -> None:
        cls._handle_users[message.chat.username] = {
            "/delSolution": [cls.startDelCommand ,cls.delEntry],
            "/getSolution": [cls.startGetCommand, cls.getEntry],
            "/addSolution": [cls.startAddCommand, cls.getEntryName, cls.getEntryFile],
        }[command]
    
    @classmethod
    def handleUserMessage(cls, message: Message) -> Union[str, BufferedReader]:
        if message.chat.username not in cls._handle_users.keys():
            return HELP_MSG
        
        is_success, result = cls._handle_users[message.chat.username][0](message)
        cls._cleanSubscribers(message.chat.username, is_success)
        
        return result
    
    @classmethod
    def _cleanSubscribers(cls, username: str, is_success: bool) -> None:
        if is_success:
            cls._handle_users[username].pop(0)
        
        if len(cls._handle_users[username]) == 0:
            cls._handle_users.pop(username)
