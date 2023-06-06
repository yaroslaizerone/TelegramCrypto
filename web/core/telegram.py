import telebot


def send_notify(message):
    bot = telebot.TeleBot("6088225226:AAFRzGugXIsh-6TATesTg85kJy4WzceEpws")
    bot.send_message(987527279, message)