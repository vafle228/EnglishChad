import os
from typing import Dict, Tuple

import requests
from ChadUtils.constants import TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.Solution.solution import SolutionLevel
from DataBase.Solution.solutionmanager import SolutionManager
from MessageStructs.basestruct import IMessage
from ProgressBar.telergambar import telegramProgressBarWrapper

from ChadLogic.replies import (ADD_FILE_ERROR_MSG, ADD_LEVEL_ERROR_MSG,
                               ADD_LEVEL_SUCCESS_MSG, ADD_NAME_ERROR_MSG,
                               ADD_NAME_SUCCESS_MSG, ADD_START_MSG,
                               ADD_SUCCESS_MSG)


class AddEntryMixin:
    _replies: Dict[str, list] = dict()

    _database = SolutionManager
    _aws_storage = ChadAWSManager.getInstance()

    @classmethod
    def startAddCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, ADD_START_MSG)

    @classmethod
    def getEntryName(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateEntryAddName(message):
            return (False, ADD_NAME_ERROR_MSG)

        cls._replies[message.username] = [message.text]
        return (True, ADD_NAME_SUCCESS_MSG)
    
    @classmethod
    def getEntryLevel(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateEntryLevel(message):
            return (False, ADD_LEVEL_ERROR_MSG)
        
        cls._replies[message.username].append(message.text)
        return (True, ADD_LEVEL_SUCCESS_MSG)

    @classmethod
    def getEntryFile(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateEntryFile(message):
            return (False, ADD_FILE_ERROR_MSG)

        cls._saveUserFile(message.file_url, message.file_name)

        username = message.username
        entry_name, entry_level = cls._replies[username]
        file_path = f"{entry_level}/{username}/{entry_name}/{message.file_name}"

        cls._aws_storage.uploadFile(file_path, telegramProgressBarWrapper(message))
        cls._database.addSolution(entry_name, username, entry_level, file_path)

        cls._replies.pop(username)
        os.remove(TEMP_ROOT.format(message.file_name))

        return (True, ADD_SUCCESS_MSG.format(entry_name))

    @classmethod
    def _saveUserFile(cls, file_url: str, file_name: str) -> None:
        with open(TEMP_ROOT.format(file_name), "wb") as file:
            file.write(cls._downloadFileFromApi(file_url))

    @classmethod
    def _downloadFileFromApi(cls, file_url: str) -> bytes:
        return requests.get(file_url).content

    @classmethod
    def _validateEntryAddName(cls, message: IMessage) -> bool:
        return message.text and not cls._database.getSolutionByName(message.text).name
    
    @classmethod
    def _validateEntryLevel(cls, message: IMessage) -> bool:
        return SolutionLevel.hasValue(message.text)

    @classmethod
    def _validateEntryFile(cls, message: IMessage) -> bool:
        return message.file_name  # Check if there is a file_name
