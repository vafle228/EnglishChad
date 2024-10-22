from math import ceil
from typing import List, Tuple

from ChadUtils.constants import ENTRY_PER_PAGE
from ChadUtils.subscriber import ChadSubscriber, Subscriptions
from DataBase.Solution.solution import Solution
from DataBase.Solution.solutionmanager import SolutionManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (EMPTY_DB_ERROR, MAX_PAGE_ERROR, PAGE_ERROR_MSG,
                               SHOW_START_MSG, SHOW_SUCCESS_MSG)


class ShowAllEntriesMixin:
    _database = SolutionManager
    _etries_list: List[Solution] = None

    @classmethod
    def startShowCommand(cls, message: IMessage) -> Tuple[bool, str]:
        if cls._etries_list is None:
            ChadSubscriber.addNewSubsciber(
                Subscriptions.DATA_BASE_UPDATE, cls._updateEntriesList
            ); cls._updateEntriesList()  # First call init
        return (True, SHOW_START_MSG.format(cls.totalPage()))
    
    @classmethod
    def showEntriesList(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validatePageValue(message):
            return (False, PAGE_ERROR_MSG)
        
        if not cls._validateMaxPage(message):
            return (False, MAX_PAGE_ERROR.format(cls.totalPage()))
        
        if len(cls._etries_list) == 0:
            return (True, EMPTY_DB_ERROR)
        
        return cls._formPageList(int(message.text)) 
    
    @classmethod
    def totalPage(cls) -> int:
        if len(cls._etries_list) == 0:
            return 1
        return ceil(len(cls._etries_list) / ENTRY_PER_PAGE)
    
    @classmethod
    def _formPageList(cls, cur_page: int) -> Tuple[bool, str]:
        entries = ""
        for i in range((cur_page - 1) * ENTRY_PER_PAGE, cur_page * ENTRY_PER_PAGE):
            if i == len(cls._etries_list):
                return (False, entries + SHOW_SUCCESS_MSG.format(cls.totalPage()))
        
            entries += f"{cls._etries_list[i].level}: {cls._etries_list[i].name}"
            
            if not cls._etries_list[i].author.isdigit():
                entries += f" от @{cls._etries_list[i].author}"
            entries += "\n"
        return (False, entries + SHOW_SUCCESS_MSG.format(cls.totalPage()))
    
    @classmethod
    def _updateEntriesList(cls, *args, **kwargs) -> None:
        cls._etries_list = cls._database.getAllSolutions()[::-1]
    
    @classmethod
    def _validatePageValue(cls, message: IMessage) -> bool:
        return message.text and message.text.isdigit()
    
    @classmethod
    def _validateMaxPage(cls, message: IMessage) -> bool:
        return 0 < int(message.text) <= cls.totalPage()
