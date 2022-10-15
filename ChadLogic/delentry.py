from typing import Tuple

from DataBase.awsmanager import ChadAWSManager
from DataBase.Solution.solutionmanager import SolutionManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (DELETE_ERROR_MSG, DELETE_START_MSG,
                               DELETE_SUCCESS_MSG)


class DeleteEntryMixin:
    _database = SolutionManager
    _aws_storage = ChadAWSManager.getInstance()

    @classmethod
    def startDelCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, DELETE_START_MSG)

    @classmethod
    def delEntry(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._hasPermission(message):
            return (False, DELETE_ERROR_MSG)

        entry_name = message.text
        entry_path = cls._database.getSolutionByName(entry_name).path

        cls._aws_storage.deleteFile(entry_path)
        cls._database.deleteSolutionByName(entry_name)

        return (True, DELETE_SUCCESS_MSG.format(entry_name))

    @classmethod
    def _hasPermission(cls, message: IMessage) -> bool:
        entry_name = message.text
        entry = cls._database.getSolutionByName(entry_name)

        return entry.name and entry.author == message.username
