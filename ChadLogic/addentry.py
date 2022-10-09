import os
from typing import Tuple

import requests
from constants import API_REQUEST, TEMP_ROOT
from DataBase.awsmanager import ChadAWSManager
from DataBase.dbmanager import ChadDataBaseManager
from telebot.types import Message

from ChadLogic.replies import (ADD_NAME_ERROR_MSG, ADD_NAME_SUCCESS_MSG,
                               ADD_START_MSG, ADD_SUCCESS_MSG)


class AddEntryMixin:
    _replies = dict()

    _database = ChadDataBaseManager()
    _aws_storage = ChadAWSManager()

    @classmethod
    def startAddCommand(cls, message: Message) -> Tuple[bool, str]:
        return (True, ADD_START_MSG)

    @classmethod
    def getEntryName(cls, message: Message) -> Tuple[bool, str]:
        if not cls._validateEntryAddName(message):
            return (False, ADD_NAME_ERROR_MSG)

        cls._replies[message.chat.username] = message.text
        return (True, ADD_NAME_SUCCESS_MSG)

    @classmethod
    def getEntryFile(cls, message: Message) -> Tuple[bool, str]:
        if not cls._validateEntryFile(message):
            return (False, ADD_NAME_ERROR_MSG)

        cls._saveUserFile(message.document.file_id, message.document.file_name)

        username = message.chat.username
        entry_name = cls._replies[username]
        file_path = f"{username}/{message.document.file_name}"

        cls._aws_storage.uploadFile(file_path)
        cls._database.addEntry(entry_name, username, file_path)

        cls._replies.pop(username)
        os.remove(TEMP_ROOT.format(message.document.file_name))

        return (True, ADD_SUCCESS_MSG.format(entry_name))

    @classmethod
    def _saveUserFile(cls, file_id, file_name) -> None:
        with open(TEMP_ROOT.format(file_name), "wb") as file:
            file.write(cls._downloadFileFromApi(file_id))
        file.close()

    @classmethod
    def _downloadFileFromApi(cls, file_id) -> bytes:
        return requests.get(API_REQUEST.format(file_id)).content

    @classmethod
    def _validateEntryAddName(cls, message: Message) -> bool:
        return message.text and not cls._database.getEntryByName(message.text)

    @classmethod
    def _validateEntryFile(cls, message: Message) -> bool:
        return message.document
