from bs4 import BeautifulSoup
import requests
from googletrans import Translator

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
