from io import BufferedReader
from pathlib import Path
from typing import Tuple, Union

from ChadUtils.constants import TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.Solution.solutionmanager import SolutionManager
from MessageStructs.basestruct import IMessage
from ProgressBar.telergambar import telegramProgressBarWrapper

from ChadLogic.replies import GET_ERROR_MSG, GET_START_MSG


class GetEntryMixin:
    _database = SolutionManager
    _aws_storage = ChadAWSManager.getInstance()

    @classmethod
    def startGetCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, GET_START_MSG)

    @classmethod
    def getEntry(cls, message: IMessage) -> Tuple[bool, Union[BufferedReader, str]]:
        if not cls._validateEntryGetName(message):
            return (False, GET_ERROR_MSG)

        entry = cls._database.getSolutionByName(message.text)
        cls._aws_storage.downloadFile(entry.path, telegramProgressBarWrapper(message))

        return (True, open(TEMP_ROOT.format(Path(entry.path).name), "rb"))

    @classmethod
    def _validateEntryGetName(cls, message: IMessage) -> bool:
        return message.text and cls._database.getSolutionByName(message.text).name
