import os
from io import BufferedReader

import telebot
from telebot.types import Message

from ChadLogic.englishchad import EnglishChadBot
from ChadUtils.constants import API_KEY
from MessageStructs.telegramstruct import TelegramMessage

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["addSolution", "getSolution", "delSolution"])
def addNewEntry(message: Message):
    command = message.text.split(" ")[0]
    tele_messsage = TelegramMessage(message, bot)
    
    EnglishChadBot.startUserHandling(tele_messsage, command)
    bot.send_message(message.chat.id, EnglishChadBot.handleUserMessage(tele_messsage))


@bot.message_handler(content_types=["document", "text"])
def replyToMessage(message: Message):
    tele_messsage = TelegramMessage(message, bot)
    result = EnglishChadBot.handleUserMessage(tele_messsage)

    if not isinstance(result, BufferedReader):
        return bot.send_message(message.chat.id, result)
        
    bot.send_document(message.chat.id, result)
    result.close(); os.remove(result.name) 


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
