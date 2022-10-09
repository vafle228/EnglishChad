import os
from io import BufferedReader
from pathlib import Path
from typing import Tuple, Union

from constants import TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.dbmanager import ChadDataBaseManager
from telebot.types import Message

from ChadLogic.replies import GET_ERROR_MSG, GET_START_MSG


class GetEntryMixin:
    _database = ChadDataBaseManager()
    _aws_storage = ChadAWSManager()

    @classmethod
    def startGetCommand(cls, message: Message) -> Tuple[bool, str]:
        return (True, GET_START_MSG)

    @classmethod
    def getEntry(cls, message: Message) -> Tuple[bool, Union[BufferedReader, str]]:
        if not cls._validateEntryGetName(message):
            return (False, GET_ERROR_MSG)

        entry = cls._database.getEntryByName(message.text)[0]
        cls._aws_storage.downloadFile(entry[3])

        file = open(TEMP_ROOT.format(Path(entry[3]).name), "rb")
        # os.remove(TEMP_ROOT.format(Path(entry[3]).name))

        return (True, file)

    @classmethod
    def _validateEntryGetName(cls, message: Message) -> bool:
        return message.text and cls._database.getEntryByName(message.text)
