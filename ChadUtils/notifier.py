from DataBase.Subscribe.subscribemanager import SubscribeManager
from telebot import TeleBot

from ChadUtils.constants import API_KEY

bot = TeleBot(API_KEY)


def notifySubscribers(level: str, solution_name: str):
    notification = f"Добавлено новое решение {solution_name} для уровня {level}"
    for subscribe in SubscribeManager.getSubscribesByLevel(level):
        bot.send_message(subscribe.chatid, notification)
