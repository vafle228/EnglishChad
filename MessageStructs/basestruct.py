from abc import ABC, abstractmethod
from typing import Union


class IMessage(ABC):
    @property
    @abstractmethod
    def text(self) -> Union[str, None]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def username(self) -> str:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def file_name(self) -> Union[str, None]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def file_url(self) -> Union[str, None]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def file_size(self) -> Union[int, None]:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def chat_id(self) -> int:
        raise NotImplementedError
    
    @property
    @abstractmethod
    def id(self) -> int:
        raise NotImplementedError
