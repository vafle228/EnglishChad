from MessageStructs.basestruct import IMessage
from typing import Tuple
from ChadLogic.replies import HELP_MSG


class HelpMessageMixin:
    @classmethod
    def sendHelpMessage(cls, message: IMessage):
        return (True, HELP_MSG)
