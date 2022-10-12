from math import ceil
from typing import List, Tuple

from ChadUtils.constants import ENTRY_PER_PAGE
from ChadUtils.subscriber import ChadSubscriber, Subscriptions
from DataBase.dbmanager import ChadDataBaseManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (EMPTY_DB_ERROR, MAX_PAGE_ERROR, PAGE_ERROR_MSG,
                               SHOW_START_MSG, SHOW_SUCCESS_MSG)


class ShowAllEntriesMixin:
    _etries_list: List[Tuple[int, str, str, str]] = None

    @classmethod
    def startShowCommand(cls, message: IMessage) -> Tuple[bool, str]:
        if cls._etries_list is None:
            cls._updateEntriesList()  # Initing array with actual db values
        return (True, SHOW_START_MSG.format(cls.total_page()))
    
    @classmethod
    def showEntriesList(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validatePageValue(message):
            return (False, PAGE_ERROR_MSG)
        
        if not cls._validateMaxPage(message):
            return (False, MAX_PAGE_ERROR.format(cls.total_page()))
        
        if len(cls._etries_list) == 0:
            return (True, EMPTY_DB_ERROR)
        
        return cls._formPageList(int(message.text)) 
    
    @classmethod
    def total_page(cls) -> int:
        if len(cls._etries_list) == 0:
            return 1
        return ceil(len(cls._etries_list) / ENTRY_PER_PAGE)
    
    @classmethod
    def _formPageList(cls, cur_page: int) -> Tuple[bool, str]:
        entries = ""
        for i in range((cur_page - 1) * ENTRY_PER_PAGE, cur_page * ENTRY_PER_PAGE):
            if i == len(cls._etries_list) - 1:
                return (False, entries + SHOW_SUCCESS_MSG.format(cls.total_page()))
            entries += f"{i + 1}: {cls._etries_list[i][2]} от @{cls._etries_list[i][1]}\n"
        return (False, entries + SHOW_SUCCESS_MSG.format(cls.total_page()))
    
    @classmethod
    def _updateEntriesList(cls, *args, **kwargs) -> None:
        cls._etries_list = ChadDataBaseManager().getAllEntries()
    
    @classmethod
    def _validatePageValue(cls, message: IMessage) -> bool:
        return message.text and message.text.isdigit()
    
    @classmethod
    def _validateMaxPage(cls, message: IMessage) -> bool:
        return int(message.text) <= cls.total_page()


ChadSubscriber.addNewSubsciber(
    Subscriptions.DATA_BASE_UPDATE, 
    ShowAllEntriesMixin._updateEntriesList
)
