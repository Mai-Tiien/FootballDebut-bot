import os

from flask import Flask, request

import telebot

TOKEN = '5482902514:AAEmM8Tv6SRi69UYVo6V09-4aq9SQp3XDMQ'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def start(message):
    if message.text == '/text':
        bot.reply_to(message, 'Hello, {name}'.format(name=message.chat.first_name), parse_mode="Markdown")
    else:
        bot.send_message(message.from_user.id, "Будь-ласка, ведіть команду /help")


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://newsfootballduet-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8443)))
