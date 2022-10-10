import os
from typing import Tuple

import requests
from ChadUtils.constants import TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.dbmanager import ChadDataBaseManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (ADD_NAME_ERROR_MSG, ADD_NAME_SUCCESS_MSG,
                               ADD_START_MSG, ADD_SUCCESS_MSG)


class AddEntryMixin:
    _replies = dict()

    _database = ChadDataBaseManager()
    _aws_storage = ChadAWSManager()

    @classmethod
    def startAddCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, ADD_START_MSG)

    @classmethod
    def getEntryName(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateEntryAddName(message):
            return (False, ADD_NAME_ERROR_MSG)

        cls._replies[message.username] = message.text
        return (True, ADD_NAME_SUCCESS_MSG)

    @classmethod
    def getEntryFile(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateEntryFile(message):
            return (False, ADD_NAME_ERROR_MSG)

        cls._saveUserFile(message.file_url, message.file_name)

        username = message.username
        entry_name = cls._replies[username]
        file_path = f"{username}/{entry_name}/{message.file_name}"

        cls._aws_storage.uploadFile(file_path)
        cls._database.addEntry(entry_name, username, file_path)

        cls._replies.pop(username)
        os.remove(TEMP_ROOT.format(message.file_name))

        return (True, ADD_SUCCESS_MSG.format(entry_name))

    @classmethod
    def _saveUserFile(cls, file_url: str, file_name: str) -> None:
        with open(TEMP_ROOT.format(file_name), "wb") as file:
            file.write(cls._downloadFileFromApi(file_url))
        file.close()

    @classmethod
    def _downloadFileFromApi(cls, file_url: str) -> bytes:
        return requests.get(file_url).content

    @classmethod
    def _validateEntryAddName(cls, message: IMessage) -> bool:
        return message.text and not cls._database.getEntryByName(message.text)

    @classmethod
    def _validateEntryFile(cls, message: IMessage) -> bool:
        return message.file_name  # Check if there is a file name
