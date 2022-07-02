from bs4 import BeautifulSoup
from selenium import webdriver
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
        template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
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

if __name__ == '__main__':
    main()