import os
from io import BufferedReader

import telebot
from telebot.types import Message

from ChadLogic.englishchad import EnglishChadBot
from ChadUtils.constants import API_KEY
from MessageStructs.telegramstruct import TelegramMessage

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=[
    "start", "help", "addsolution", 
    "getsolution", "delsolution", "showsolution", 
    "subscribe", "unsubscribe"
])
def addNewEntry(message: Message) -> None:
    command = message.text.split(" ")[0]
    tele_messsage = TelegramMessage(message, bot)
    
    EnglishChadBot.startUserHandling(tele_messsage, command)
    bot.send_message(message.chat.id, EnglishChadBot.handleUserMessage(tele_messsage))


@bot.message_handler(content_types=["document", "text"])
def replyToMessage(message: Message) -> None:
    message = removeErrorSymbols(message)
    tele_messsage = TelegramMessage(message, bot)
    result = EnglishChadBot.handleUserMessage(tele_messsage)

    if not isinstance(result, BufferedReader):
        return bot.send_message(message.chat.id, result)
    
    bot.send_document(message.chat.id, result)
    result.close(); os.remove(result.name)


def removeErrorSymbols(message: Message) -> Message:
    if message.text is not None:
        message.text = message.text.replace("'", "")
    if message.from_user.username is not None:
        message.from_user.username = message.from_user.username.replace("'", "")
    return message


def bot_polling() -> None:
    while "Bot polling loop":
        try:
            print("New bot instance started")
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Bot failed with \n{e}")
            bot.stop_polling()


if __name__ == "__main__": bot_polling()
