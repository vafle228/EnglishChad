from typing import Tuple

from DataBase.Solution.solution import SolutionLevel
from DataBase.Subscribe.subscribemanager import SubscribeManager
from MessageStructs.basestruct import IMessage

from ChadLogic.replies import (UNSUBSCRIBE_ERROR_MSG, UNSUBSCRIBE_EXISTS_MSG,
                               UNSUBSCRIBE_START_MSG, UNSUBSCRIBE_SUCCESS_MSG)


class UnsubscribeUserMixin:
    @classmethod
    def startUnsubcribeCommand(cls, message: IMessage) -> Tuple[bool, str]:
        return (True, UNSUBSCRIBE_START_MSG)
    
    @classmethod
    def unsubscribeUser(cls, message: IMessage) -> Tuple[bool, str]:
        if not cls._validateUnsubscribeLevel(message):
            return (False, UNSUBSCRIBE_ERROR_MSG)
        
        if not cls._isSubscribeExists(message):
            return (True, UNSUBSCRIBE_EXISTS_MSG)
        
        SubscribeManager.deleteSubscribeById(
            SubscribeManager.getSubscribe(message.text, message.chat_id).id
        ); return (True, UNSUBSCRIBE_SUCCESS_MSG)

    @classmethod
    def _validateUnsubscribeLevel(cls, message: IMessage) -> bool:
        return SolutionLevel.hasValue(message.text)
    
    @classmethod
    def _isSubscribeExists(cls, message: IMessage) -> bool:
        return SubscribeManager.getSubscribe(message.text, message.chat_id).id
