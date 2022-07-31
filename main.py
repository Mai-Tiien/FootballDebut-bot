import telebot
import os
from flask import Flask, request

TOKEN = '5499977311:AAFd2fY862MCTE8c4JNvcDybVCWXZQxS-Sg'
APP_NAME='https://footballduet-bot.herokuapp.com/'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

@bot.message_handler(content_types=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привіт, надсилай свої ідеї чи контент")  
    else:
        bot.send_message(message.from_user.id, "Помилка! Буль-ласка, повторіть ще раз!")          

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    if message.content_type == 'photo':  
        img = message.photo[2].file_id
        bot.send_message(986817461, "Запит від @{name} десь там 👇".format(name=message.chat.username), parse_mode="Markdown")
        bot.send_photo(986817461, img, message.caption)
        bot.reply_to(message, "Дякую *{name}* за співпрацю! Контент відправлено на огляд.".format(name=message.chat.first_name, text=message.text), parse_mode="Markdown")
    else:
        bot.send_message(986817461, "Запит від @{name} десь там 👇".format(name=message.chat.username), parse_mode="Markdown")
        bot.send_message(986817461, message.text)
        bot.reply_to(message, "Дякую *{name}* за співпрацю! Контент відправлено на огляд.".format(name=message.chat.first_name, text=message.text), parse_mode="Markdown")
    
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "Hello, world!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_NAME + TOKEN)
    return "Hello, world!", 200    

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
