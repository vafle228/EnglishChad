from abc import ABC, abstractmethod
from MessageStructs.basestruct import IMessage


class IProgressBar(ABC):
    def __init__(self, total_size) -> None:
        self._current_size = 0
        self._total_size = total_size

        self._message = self._sendInitialMessgae("0 %")
    
    def updateProgress(self, downloaded) -> None:
        self._current_size += downloaded
        progress = (self._current_size / self._total_size) * 100

        return self._updateMessage(f"{round(progress, 2)} %")
    
    @abstractmethod
    def _updateMessage(self, text: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def _sendInitialMessgae(self, text: str) -> IMessage:
        raise NotImplementedError