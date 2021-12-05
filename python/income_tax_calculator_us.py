from bs4 import BeautifulSoup
import requests
import sys
# geting income tax information from website
def get_income_tax_info(flag):
    map = list()
    if flag:
        # get website html
        html = requests.get("https://www.bankrate.com/finance/taxes/tax-brackets.aspx")
        soup = BeautifulSoup(html.text, 'html.parser')
        # finding the table with the income tax information
        context = soup.find('tbody')
        # geting all rows in table
        trs = context.find_all("tr")
        # looping though rows
        for tr in trs:
            lines = list()
            # get first two cell in row cell 1 is the level and cell 2 is the range
            tds = tr.find_all("td")[:2]
            numeric_filter = filter(str.isdigit, tds[0].text)
            lines.append(int("".join(numeric_filter)))
            range = tds[1].text.split(' ')
            numeric_filter = filter(str.isdigit, range[0])
            lines.append(int("".join(numeric_filter)))
            numeric_filter = filter(str.isdigit, range[2])
            # if range don't have max value then put the maximum value of int as max value
            try:
                lines.append(int("".join(numeric_filter)))
            except:
                lines.append(sys.maxsize)
            map.append(lines)
    else:
        for row in open("../resource/income_tax_calculator_us/tax_info.txt", "r").read().splitlines():
            lines = list()
            # get first two cell in row cell 1 is the level and cell 2 is the range
            tds = row.split('|')
            numeric_filter = filter(str.isdigit, tds[0])
            lines.append(int("".join(numeric_filter)))
            range = tds[1].split(' ')
            numeric_filter = filter(str.isdigit, range[0])
            lines.append(int("".join(numeric_filter)))
            numeric_filter = filter(str.isdigit, range[2])
            # if range don't have max value then put the maximum value of int as max value
            try:
                lines.append(int("".join(numeric_filter)))
            except:
                lines.append(sys.maxsize)
            map.append(lines)
    #returning a matrix with the clean information
    return map
# calculating your income tax
def income_tax_calculetor(income,internet=True):
    #geting the income tax information
    map=list()
    tax=0
    map=get_income_tax_info(internet)
    # looping through levels of income
    for level in map:
        # if current level is your max income level then add tis level tax to the totall tax else add max amount of tax of this level
        if income >= level[1] and income <= level[2]:
            tax+=(income-(level[1]-(1 if level[1]>0 else 0)))*(level[0]/100.0)
            break
        else:
            tax+=(level[2]-(level[1]-(1 if level[1]>0 else 0)))*(level[0]/100.0)
    #return the amount of income tax and your income after tax
    return tax , income-tax
# add ',' to number for better visualisation
def number_butifier(number):
    # split the number to int part and float part of the number
    num1=str(number).split(".")
    # add a '.' in the middle of the list if the number have float part
    if len(num1)==2:
        num1.insert(1,".")
    #looping through every char in the int part and add ',' every 3 cells
    num1[0]="".join(l+","*(n%3==2) for n,l in enumerate(num1[0][::-1]))[::-1]
    #if there a extra ',' then delete it
    if num1[0][0]==',':
        num1[0]=num1[0][1:]
    #returning the butifier number
    return "".join(num1)
#user gui
def main():
    print("enter your total income")
    income=float(input())
    tax,remain=income_tax_calculetor(income,False)
    print('total tax:{}\nincome after tax:{}\ntax percentage:{}'.format(number_butifier(tax),number_butifier(remain),(tax/income)*100.0))
if __name__ == '__main__':
    main()