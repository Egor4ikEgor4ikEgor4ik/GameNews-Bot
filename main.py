import os
from textwrap import dedent
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import telegram
from time import sleep

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

def build_post_coopland(headline_coopland,description_coopland,post_url_coopland):
    post_coopland_text = dedent(f'''{headline_coopland}  
    {description_coopland}    
Ссылка на источник: {post_url_coopland} ''')     
    return post_coopland_text


def save_and_download_image(picture_url,photo_path):
        response = requests.get(picture_url)
        with open(photo_path, "wb") as file:
            file.write(response.content)
        return response
    


if __name__ == "__main__":
    
    telegram_bot_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = '@gamingnewsfornerds'

    
    while True:
        headline_coopland,description_coopland,picture_url_coopland,post_url_coopland = get_last_news_coopland()

        save_and_download_image(
        picture_url=picture_url_coopland,
        photo_path = './images_coopland/bebra_coopland.png'
        )
        
        
        with open("last_saved_post.json", "r", encoding="CP1251") as my_file:
            file_contents = my_file.read()
        file_contents = json.loads(file_contents)
        
        if headline_coopland not in file_contents:
            
            bot = telegram.Bot(token=telegram_bot_token)
            bot.send_photo(chat_id=telegram_chat_id, photo=open('./images_coopland/bebra_coopland.png', 'rb'),caption=build_post_coopland(headline_coopland,description_coopland,post_url_coopland))
            
            with open("last_saved_post.json", "w", encoding="CP1251") as my_file:
                file_contents.append(headline_coopland)
                my_file.write(json.dumps(file_contents))
        sleep(3600)









