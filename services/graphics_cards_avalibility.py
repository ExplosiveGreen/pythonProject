from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import re
import os
msrp = {
    'rtx 3060':329.0,
    'rtx 3060 ti':399.0,
    'rtx 3070': 499.0,
    'rtx 3070 ti': 599.0,
    'rtx 3080':699.0,
    'rtx 3080 ti':1199.0,
    'rtx 3090':1499.0
}


def get_url(website,search_term):
    template = ""
    if website == "amazon":
        template = 'https://www.amazon.com/s?k={}&currency=USD&ref=nb_sb_noss_1'
    search_term=search_term.replace(' ', '+')
    return template.format(search_term)


def get_amazon_prices(driver,search_term):
    url = get_url('amazon', search_term)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    products = list()
    for item in results:
        atag = item.h2.a
        title = atag.text.strip()
        url = 'https://www.amazon.com' + atag.get('href')
        price = 0
        try:
            price_parent = item.find('span', 'a-price')
            price_off = price_parent.find('span', 'a-offscreen')
            price = float(price_off.text.replace('$', "").replace(',', ''))
        except Exception as e:
            price = 1000000
        if all(word in title.lower() for word in search_term.lower().split(" ")) and price >= 0.5*msrp[search_term]:
            products.append((url, price))
    return products


def main():
    PATH=os.path.dirname(__file__)+"\\resource\graphics_cards_avalibility\chromedriver.exe"
    search_terms = ['rtx 3060', 'rtx 3060 ti', 'rtx 3070', 'rtx 3070 ti', 'rtx 3080', 'rtx 3080 ti', 'rtx 3090']
    driver = webdriver.Chrome(PATH)
    result = list()
    for search_term in search_terms:
        product = min(get_amazon_prices(driver, search_term), key=lambda item: item[1])
        result.append([search_term, product[1], product[1] <= msrp[search_term]])
    print(result)
    return {'result': result}
def sortp(a):
    return a[1]
if __name__ == '__main__':
    #main()
    soup = BeautifulSoup(requests.get(get_url('amazon', 'rtx 3060'),headers={
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
    }).text, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    products = list()
    for item in results:
        atag = item.h2.a
        title = atag.text.strip()
        url = 'https://www.amazon.com' + atag.get('href')
        price = 0
        try:
            price_parent = item.find('span', 'a-price')
            price_off = price_parent.find('span', 'a-offscreen')
            price = float(price_off.text.replace('$','').replace(',',''))
        except Exception as e:
            price = 1000000
        print(url,price)
        if all(word in title.lower() for word in 'rtx 3060'.lower().split(" ")) and price >= 0.5 * msrp['rtx 3060']:
            products.append((url,price))
    products.sort(key=sortp)