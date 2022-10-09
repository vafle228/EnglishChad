from typing import Tuple

from DataBase.awsmanager import ChadAWSManager
from DataBase.dbmanager import ChadDataBaseManager
from telebot.types import Message

from ChadLogic.replies import (DELETE_ERROR_MSG, DELETE_START_MSG,
                               DELETE_SUCCESS_MSG)


class DeleteEntryMixin:
    _database = ChadDataBaseManager()
    _aws_storage = ChadAWSManager()

    @classmethod
    def startDelCommand(cls, message: Message) -> Tuple[bool, str]:
        return (True, DELETE_START_MSG)

    @classmethod
    def delEntry(cls, message: Message) -> Tuple[bool, str]:
        if not cls._hasPermission(message):
            return (False, DELETE_ERROR_MSG)

        entry_name = message.text
        entry_path = cls._database.getEntryByName(entry_name)[0][3]

        cls._aws_storage.deleteFile(entry_path)
        cls._database.deleteEntryByNames(entry_name)

        return (True, DELETE_SUCCESS_MSG.format(entry_name))

    @classmethod
    def _hasPermission(cls, message: Message) -> bool:
        entry_name = message.text
        entry = cls._database.getEntryByName(entry_name)

        return entry and entry[0][1] == message.chat.username
