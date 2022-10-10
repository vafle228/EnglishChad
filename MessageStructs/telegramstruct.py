from telebot.types import Message
from telebot import TeleBot
from MessageStructs.basestruct import IMessage
from ChadUtils.constants import API_REQUEST
from typing import Union


class TelegramMessage(IMessage):
    def __init__(self, message: Message, tele_bot: TeleBot) -> None:
        self._message = message
        self._tele_bot = tele_bot
    
    @property
    def username(self) -> str:
        return self._message.chat.username
    
    @property
    def text(self) -> Union[str, None]:
        return self._message.text
    
    @property
    def file_name(self) -> Union[str, None]:
        if self._message.document:
            return self._message.document.file_name
    
    @property
    def file_url(self) -> Union[str, None]:
        if self._message.document:
            file_info = self._tele_bot.get_file(self._file_id)
            return API_REQUEST + file_info.file_path
    
    @property
    def _file_id(self) -> Union[str, None]:
        if self._message.document:
            return self._message.document.file_id
