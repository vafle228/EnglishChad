import telebot
from ChadLogic.englishchad import EnglishChadBot
from telebot.types import Message
from io import BufferedReader

from constants import API_KEY

bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['addSolution'])
def addNewEntry(message: Message):
    EnglishChadBot.startUserHandling(message, "/addSolution")
    bot.send_message(message.chat.id, EnglishChadBot.handleUserMessage(message))


@bot.message_handler(commands=['getSolution'])
def getEntryByName(message: Message):
    EnglishChadBot.startUserHandling(message, "/getSolution")
    bot.send_message(message.chat.id, EnglishChadBot.handleUserMessage(message))


@bot.message_handler(commands=['delSolution'])
def deleteEntryByName(message: Message):
    EnglishChadBot.startUserHandling(message, "/delSolution")
    bot.send_message(message.chat.id, EnglishChadBot.handleUserMessage(message))


@bot.message_handler(content_types=["document", "text"])
def replyToMessage(message: Message):
    result = EnglishChadBot.handleUserMessage(message)

    if isinstance(result, BufferedReader):
        bot.send_document(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, result)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
