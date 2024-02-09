from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
from geopy.geocoders import Nominatim
import json
from pymongo import MongoClient
from dotenv import load_dotenv


def main():
    start = time.time()
    results = list()
    geolocator = Nominatim(user_agent="GiveHub")
    path = os.path.dirname(__file__) + "\\resource\\graphics_cards_avalibility\\chromedriver.exe"
    url = 'https://www.guidestar.org.il/search-malkars?Sug_Hitagdut=%D7%A2%D7%9E%D7%95%D7%AA%D7%94&AidToCivilians=604'
    try:
        driver = webdriver.Chrome(path)
        driver.get(url)
    except:
        driver = webdriver.Chrome(path)
        driver.get(url)
    start_height = 0
    new_height = driver.execute_script("return document.body.scrollHeight")
    while start_height < new_height:
        driver.execute_script(f'window.scrollTo({start_height}, {new_height});')
        time.sleep(1)
        start_height = new_height
        new_height = driver.execute_script("return document.body.scrollHeight")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for org in (soup.find_all('app-search-result-item')):
        org = (org.find('div', {'class': 'search-result-item-wrapper'})
               .find('div', {'class': 'search-result-item-container'})
               .find('div', {'class': 'search-result-item-main-block'}))
        name = org.find('h2', {'class': 'search-result-item-name'}).text.strip()
        address = ",".join(org.find('div', {'class': 'search-result-item-activity-container'})
                           .find_all('app-label-value', {'class': 'search-result-item-data'})[2]
                           .find('div').find_all('span')[3].text.strip().split(',')[0:-1])
        try:
            location = geolocator.geocode(address)
        except:
            geolocator = Nominatim(user_agent="GiveHub")
            location = geolocator.geocode(address)

        if location:
            link = f"https://www.guidestar.org.il{org.find('a').get('href')}/contact"
            try:
                driver.get(link)
            except:
                driver = webdriver.Chrome(path)
                driver.get(link)
            time.sleep(1)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            img = soup2.find('img', {'alt': 'email icon'})
            if img:
                email = img.next.text.strip()
                results.append({
                    'name': name,
                    'location': (location.latitude, location.longitude),
                    'email': email
                })
    driver.close()
    print(f'time to fetch:{time.time() - start}')
    save_to_mongo(results)


def save_to_mongo(data):
    load_dotenv()
    with MongoClient(os.getenv('MONGO_URI')) as client:
        db = client['GiveHub']
        collection = db['organizations']
        results = collection.insert_many(data)
        print(f'{len(results.inserted_ids)}:{results.inserted_ids}')


def save_to_json(data):
    with open('resource/GiveHub-scraping/organizations.json', 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    main()
