import telebot
from flask import Flask, request

from ChadUtils.constants import SERVER_HOOK
from telegrambot import bot


bot.remove_webhook(); bot.set_webhook(SERVER_HOOK)

app = Flask(__name__)

@app.route("/", methods=["POST"])
def englishChadWebhook():
    update_json = request.stream.read().decode("utf-8")
    telegram_update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([telegram_update])
    
    return ("Ok", 200)
