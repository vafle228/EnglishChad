from enum import Enum
from typing import Callable


class Subscriptions(str, Enum):
    DATA_BASE_UPDATE = "db_update"


class ChadSubscriber:
    _subscriptions = dict()

    @classmethod
    def addNewSubsciber(cls, event: str, callback: Callable) -> None:
        if event not in cls._subscriptions.keys():
            cls._subscriptions[event] = []
        cls._subscriptions[event].append(callback)
    
    @classmethod
    def emitToSubscribers(cls, event: str, *args, **kwargs) -> None:
        if event not in cls._subscriptions.keys():
            return None
        [cb(*args, **kwargs) for cb in cls._subscriptions[event]]