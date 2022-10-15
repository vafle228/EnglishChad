from typing import Tuple

from DataBase.Solution.solution import SolutionLevel
from DataBase.Subscribe.subscribemanager import SubscribeManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (SUBSCRIBE_ERROR_MSG, SUBSCRIBE_EXISTS_MSG,
                               SUBSCRIBE_START_MSG, SUBSCRIBE_SUCCESS_MSG)


class SubscribeUserMixin:
    @classmethod
    def startSubscribeCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, SUBSCRIBE_START_MSG)
    
    @classmethod
    def subscribeUser(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateSubscribeLevel(message):
            return (False, SUBSCRIBE_ERROR_MSG)
        
        if cls._isSubscribeExists(message):
            return (False, SUBSCRIBE_EXISTS_MSG)
        
        SubscribeManager.addSubscribe(message.text, message.chat_id)
        return (True, SUBSCRIBE_SUCCESS_MSG)


    @classmethod
    def _validateSubscribeLevel(cls, message: IMessage) -> bool:
        return SolutionLevel.hasValue(message.text)
    
    @classmethod
    def _isSubscribeExists(cls, message: IMessage) -> bool:
        return SubscribeManager.getSubscribe(message.text, message.chat_id).id
