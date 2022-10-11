from ChadUtils.constants import API_KEY
from MessageStructs.telegramstruct import IMessage, TelegramMessage
from telebot import TeleBot

from ProgressBar.progressbase import IProgressBar

bot = TeleBot(API_KEY)


def telegramProgressBarWrapper(message: IMessage):

    class TelegramProgressBar(IProgressBar):
        def _sendInitialMessgae(self, text: str) -> IMessage:
            return TelegramMessage(bot.send_message(message.chat_id, text), bot)
        
        def _updateMessage(self, text: str) -> None:
            result = bot.edit_message_text(text, self._message.chat_id, self._message.id)
            if not isinstance(result, bool):
                self._message = TelegramMessage(result, bot)
    
    return TelegramProgressBar
