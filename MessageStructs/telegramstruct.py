from telebot.types import Message
from telebot import TeleBot
from MessageStructs.basestruct import IMessage
from ChadUtils.constants import API_REQUEST
from typing import Union
from ChadUtils.constants import MAX_FILE_SIZE


class TelegramMessage(IMessage):
    def __init__(self, message: Message, bot: TeleBot) -> None:
        self._message = message

        self._file_info = None
        if message.document is not None and message.document.file_size < MAX_FILE_SIZE:
            self._file_info = bot.get_file(message.document.file_id)
    
    @property
    def username(self) -> str:
        return self._message.from_user.username or self._message.from_user.id
    
    @property
    def text(self) -> Union[str, None]:
        return self._message.text
    
    @property
    def file_name(self) -> Union[str, None]:
        if self._file_info is None:
            return None
        return self._file_info.file_path.split("/")[-1]
    
    @property
    def file_url(self) -> Union[str, None]:
        if self._file_info is None:
            return None
        return API_REQUEST + self._file_info.file_path
    
    @property
    def file_size(self) -> Union[int, None]:
        if self._file_info is None:
            return None
        return self._file_info.file_size
    
    @property
    def chat_id(self) -> int:
        return self._message.chat.id
    
    @property
    def id(self) -> int:
        return self._message.id
