from enum import Enum
from typing import Callable, Dict, List


class Subscriptions(str, Enum):
    DATA_BASE_UPDATE = "db_update"
    SOLUTION_ADD = "solution_add"


class ChadSubscriber:
    _subscriptions: Dict[str, List[Callable]] = dict()

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
