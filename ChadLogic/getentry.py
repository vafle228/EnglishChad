from io import BufferedReader
from pathlib import Path
from typing import Tuple, Union

from ChadUtils.constants import TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.dbmanager import ChadDataBaseManager
from MessageStructs.basestruct import IMessage
from ProgressBar.telergambar import telegramProgressBarWrapper

from ChadLogic.replies import GET_ERROR_MSG, GET_START_MSG


class GetEntryMixin:
    _aws_storage = ChadAWSManager().getInstance()
    _database = ChadDataBaseManager().getInstance()

    @classmethod
    def startGetCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, GET_START_MSG)

    @classmethod
    def getEntry(cls, message: IMessage) -> Tuple[bool, Union[BufferedReader, str]]:
        if not cls._validateEntryGetName(message):
            return (False, GET_ERROR_MSG)

        entry = cls._database.getEntryByName(message.text)[0]
        cls._aws_storage.downloadFile(entry[3], telegramProgressBarWrapper(message))

        return (True, open(TEMP_ROOT.format(Path(entry[3]).name), "rb"))

    @classmethod
    def _validateEntryGetName(cls, message: IMessage) -> bool:
        return message.text and cls._database.getEntryByName(message.text)
