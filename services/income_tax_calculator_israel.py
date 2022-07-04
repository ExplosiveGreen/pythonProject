import requests
from bs4 import BeautifulSoup
from datetime import date
from os.path import exists
import sys


def isNumber(str1):
    return str.isdigit(str1) or str1 == '.'


# getting income tax information from website
def get_tax_info(flag):
    income_tax_map = list()
    social_tax_map = list()
    health_tax_map = list()
    current_year = date.today().year
    # if tax info file not exist and internet flag is true then download tax info file
    if flag and (not exists(f'resource/income_tax_calculator_israel/income_tax_{current_year}.txt')
                 or not exists(f'resource/income_tax_calculator_israel/health_tax_{current_year}.txt')
                 or not exists(f'resource/income_tax_calculator_israel/social_tax_{current_year}.txt')):
        try:
            # get website tax bracket
            html = requests.get(
                "https://www.kolzchut.org.il/he/%D7%9E%D7%93%D7%A8%D7%92%D7%95%D7%AA_%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94")
            soup = BeautifulSoup(html.text, 'html.parser')
            tax_table = soup.find('table', {'class': 'wikitable'}).tbody.find_all('tr')[1:]
            for row in tax_table:
                year, _, percent = row.find_all('td')
                numeric_filter = filter(isNumber, percent.text)
                pay_range = year.text.replace('₪', '').replace('-', '').replace(' ומעלה', 'moree').replace('עד', '0')[
                            :-1].split(" ")
                line = f'{"".join(numeric_filter)} {" ".join(pay_range)}'
                income_tax_map.append(line)
            # get tax subtraction
            html = requests.get(
                "https://www.kolzchut.org.il/he/%D7%A0%D7%A7%D7%95%D7%93%D7%95%D7%AA_%D7%96%D7%99%D7%9B%D7%95%D7%99_%D7%9E%D7%9E%D7%A1_%D7%94%D7%9B%D7%A0%D7%A1%D7%94")
            soup = BeautifulSoup(html.text, 'html.parser')
            numeric_filter = filter(isNumber, soup.find('div', {'class': 'article-summary'}).div.div.div.text)
            points_val = "".join(numeric_filter)
            # get social and health tax bracket
            html = requests.get(
                "https://www.btl.gov.il/Insurance/Rates/Pages/%D7%9C%D7%A2%D7%95%D7%91%D7%93%D7%99%D7%9D%20%D7%A9%D7%9B%D7%99%D7%A8%D7%99%D7%9D.aspx")
            soup = BeautifulSoup(html.text, 'html.parser')
            tax_table = soup.find('table', {'class': 'btl-rteTable-default'}).tbody.find_all('tr')
            # first bracket
            numeric_filter = filter(isNumber, tax_table[2].find_all('td')[1].span.text)
            social_percent = "".join(numeric_filter)
            numeric_filter = filter(isNumber, tax_table[3].find_all('td')[1].span.text)
            health_percent = "".join(numeric_filter)
            numeric_filter = filter(isNumber, tax_table[0].find_all('th')[1].strong.span.text)
            end = "".join(numeric_filter)
            line = ' '.join([social_percent, '0', end])
            social_tax_map.append(line)
            line = ' '.join([health_percent, '0', end])
            health_tax_map.append(line)
            # second bracket
            numeric_filter = filter(isNumber, tax_table[2].find_all('td')[4].span.text)
            social_percent = "".join(numeric_filter)
            numeric_filter = filter(isNumber, tax_table[3].find_all('td')[4].span.text)
            health_percent = "".join(numeric_filter)
            numeric_filter = filter(isNumber, tax_table[0].find_all('td')[0].strong.span.text)
            max_end = "".join(numeric_filter)
            line = ' '.join([social_percent, str(float(end) + 1), max_end])
            social_tax_map.append(line)
            line = ' '.join([health_percent, str(float(end) + 1), max_end])
            health_tax_map.append(line)
            income_tax_table = "\n".join(income_tax_map)
            income_tax_content = f'{points_val}\n{income_tax_table}'
            social_tax_table = "\n".join(social_tax_map)
            social_tax_content = social_tax_table
            health_tax_table = "\n".join(health_tax_map)
            health_tax_content = health_tax_table
            open(f'resource/income_tax_calculator_israel/income_tax_{current_year}.txt', 'w').write(income_tax_content)
            open(f'resource/income_tax_calculator_israel/social_tax_{current_year}.txt', 'w').write(social_tax_content)
            open(f'resource/income_tax_calculator_israel/health_tax_{current_year}.txt', 'w').write(health_tax_content)
        # if error happened while downloading exist program
        except requests.ConnectionError:
            print("Connection Error")
            exit(1)
    if (exists(f'resource/income_tax_calculator_israel/income_tax_{current_year}.txt')
            and exists(f'resource/income_tax_calculator_israel/health_tax_{current_year}.txt')
            and exists(f'resource/income_tax_calculator_israel/social_tax_{current_year}.txt')):
        income = open(f'resource/income_tax_calculator_israel/income_tax_{current_year}.txt', 'r').read().replace(',',
                                                                                                                  '').split(
            '\n')
        social = open(f'resource/income_tax_calculator_israel/social_tax_{current_year}.txt', 'r').read().replace(',',
                                                                                                                  '').split(
            '\n')
        health = open(f'resource/income_tax_calculator_israel/health_tax_{current_year}.txt', 'r').read().replace(',',
                                                                                                                  '').split(
            '\n')
        table = list()
        for row in income[1:]:
            percent, start, end = row.split(' ')
            table.append([float(percent), float(start), float(sys.maxsize if end == 'more' else end)])
        income_tax = {
            'points_val': float(income[0]),
            'tax_table': table
        }
        table = list()
        for row in social:
            percent, start, end = row.split(' ')
            table.append([float(percent), float(start), float(end)])
        social_tax = {
            'tax_table': table
        }
        table = list()
        for row in health:
            percent, start, end = row.split(' ')
            table.append([float(percent), float(start), float(end)])
        health_tax = {
            'tax_table': table
        }
        return [income_tax, social_tax, health_tax]


# calculating your income tax
def tax_calculator(income, internet=True):
    income_tax = 0
    social_tax = 0
    health_tax = 0
    income_tax_info, social_tax_info, health_tax_info = get_tax_info(internet)
    for bracket in income_tax_info['tax_table']:
        percent, start, end = bracket
        if income * 12 < start:
            break
        if income * 12 <= end:
            income_tax += (income * 12 - start + (1 if start != 0 else 0)) * (percent / 100)
        elif income * 12 > end:
            income_tax += (end - start + (1 if start != 0 else 0)) * (percent / 100)
    income_tax -= 2.25 * income_tax_info['points_val']
    income_tax /= 12
    for bracket in social_tax_info['tax_table']:
        percent, start, end = bracket
        if income < start:
            break
        if income <= end:
            social_tax += (income - start + (1 if start != 0 else 0)) * (percent / 100)
        elif income > end:
            social_tax += (end - start + (1 if start != 0 else 0)) * (percent / 100)
    for bracket in health_tax_info['tax_table']:
        percent, start, end = bracket
        if income < start:
            break
        if income <= end:
            health_tax += (income - start + (1 if start != 0 else 0)) * (percent / 100)
        elif income > end:
            health_tax += (end - start + (1 if start != 0 else 0)) * (percent / 100)
    return [round(income_tax), round(social_tax), round(health_tax)]


# add ',' to number for better visualisation
def number_beautifier(number):
    # split the number to int part and float part of the number
    num1 = str(number).split(".")
    # add a '.' in the middle of the list if the number have float part
    if len(num1) == 2:
        num1.insert(1, ".")
    # looping through every char in the int part and add ',' every 3 cells
    num1[0] = "".join(l + "," * (n % 3 == 2) for n, l in enumerate(num1[0][::-1]))[::-1]
    # delete ',' if exist an extra
    if num1[0][0] == ',':
        num1[0] = num1[0][1:]
    # returning the beautifier number
    return "".join(num1)


# user gui
def main(income, crypto, choice, stock, losses):
    if choice == 'y' or crypto > 10000:
        income += crypto
    else:
        stock += crypto
    income_tax, social_tax, health_tax = tax_calculator(income)
    stock_tax = stock * 0.25 if stock > 0 else stock
    result = {
        "stock tax": number_beautifier(stock_tax if stock_tax > 0 else 0),
        "income tax": number_beautifier(income_tax),
        "social tax": number_beautifier(social_tax),
        "health tax": number_beautifier(health_tax),
        "losses discount": number_beautifier(losses - (stock_tax if stock_tax < 0 else 0)),
        "total tax": number_beautifier(income_tax + social_tax + health_tax + stock_tax - losses),
        "salary after tax": number_beautifier(
            income + (stock if stock > 0 else 0) - (income_tax + social_tax + health_tax + stock_tax - losses)),
        "tax rate": f'{number_beautifier((income_tax + social_tax + health_tax + stock_tax - losses) / (income + (stock if stock > 0 else 0)) * 100.0)}%'
    }
    print(result)
    return {"result": result}


if __name__ == '__main__':
    main(10956, 0, 'n', 0, 0)
