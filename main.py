import telebot
import os
from flask import Flask, request
from bs4 import BeautifulSoup
import requests
from googletrans import Translator

TOKEN = '5499977311:AAFd2fY862MCTE8c4JNvcDybVCWXZQxS-Sg'
APP_NAME='https://footballduet-bot.herokuapp.com/'
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)       

headers = {'User-agent': 'Mozilla/5.0'}

request = requests.get('https://www.skysports.com/football/news', headers=headers)
html = request.content

soup = BeautifulSoup(html, 'html.parser')

def football(keyword):
    news_list = []

    for h in soup.findAll('a', class_='news-list__headline-link'):
        news_title = h.contents[0].lower()

        if news_title not in news_list:
            if 'skysports' not in news_title:
                news_list.append(news_title)

    with open('out.txt', 'w', encoding='utf-8') as file:
        for i, title in enumerate(news_list):
            text = title.strip()
            translator = Translator()
            trans = translator.translate(text, dest='ru')
            res = i+1, trans.text
            
            tee = str(res)+'\n'
            file.write(tee.replace("(", "").replace(")","").replace("'","").replace(",","."))
    with open('out.txt', encoding='utf-8') as f:
        contents = f.read()        
    return contents

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo'])
def echo_message(message):
    # if message.text == '/start':
    #     bot.send_message(message.from_user.id, "Привіт, надсилай свої ідеї чи контент")
    if message.text == "/news":
        bot.send_message(message.from_user.id, "Йде процес обробки... Будь-Ласка нічого не пишить!")
        bot.send_message(message.from_user.id, football("football"))      
    elif message.content_type == 'photo':  
        img = message.photo[2].file_id
        bot.send_message(986817461, "Запит від @{name} десь там 👇".format(name=message.chat.username), parse_mode="Markdown")
        bot.send_photo(986817461, img, message.caption)
        bot.reply_to(message, "Дякую *{name}* за співпрацю! Контент відправлено на огляд.".format(name=message.chat.first_name, text=message.text), parse_mode="Markdown")    
    else:
        bot.send_message(986817461, "Запит від @{name} десь там 👇".format(name=message.chat.username), parse_mode="Markdown")
        bot.send_message(986817461, message.text)
        bot.reply_to(message, "Дякую *{name}* за співпрацю! Контент відправлено на огляд.".format(name=message.chat.first_name, text=message.text), parse_mode="Markdown")
      

@bot.message_handler(func=lambda message: True, content_types=['video', 'video_note'])
def echo_video(message):
    bot.send_message(986817461, "Відправка відео від @{name} десь там 👇".format(name=message.chat.first_name), parse_mode="Markdown")
    bot.send_video(986817461, message.video.file_id, timeout=10)
    bot.reply_to(message, "Дякую за відео-контент! Контент відправлено на огляд.")
    
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
