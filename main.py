import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import telegram

load_dotenv()


def get_last_news_coopland():
    response = requests.get("https://coop-land.ru/helpguides/new/")
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, features="html.parser")
    headline = soup.find('h2').text
    description = soup.find('div', class_="preview-text").text
    picture = soup.find('div',class_="image").find('img')["data-src"]
    picture_url =  f'https://coop-land.ru{picture}'
    post_url = soup.find('a', class_="big-link")['href']
    return headline,description,picture_url,post_url









headline_coopland,description_coopland,picture_url_coopland,post_url_coopland = get_last_news_coopland()
#print (headline_coopland,description_coopland,picture_url_coopland,post_url_coopland)

response = requests.get(picture_url_coopland)
with open(f'./images_coopland/bebra_coopland.png', "wb") as file:    
            file.write(response.content)
post_coopland = (f'''{headline_coopland}

{description_coopland}

Ссылка на источник: {post_url_coopland}

''')

telegram_bot_token = os.getenv("BOT_TOKEN")
telegram_chat_id = '@gamingnewsfornerds'

bot = telegram.Bot(token=telegram_bot_token)
bot.send_photo(chat_id=telegram_chat_id, photo=open('./images_coopland/bebra_coopland.png', 'rb'),caption=post_coopland)
# def replace_o_to_A(old_text):
#     new_text = old_text.replace('о', "А")
#     return new_text


# text1 = "Привет, меня зовут Егор"
# result_text_good1 = replace_o_to_A(old_text=text1)

# text2 = "Привет, меня зовут олег"
# result_text_good2 = replace_o_to_A(old_text=text2)
# print(result_text_good1)
# print(result_text_good2)