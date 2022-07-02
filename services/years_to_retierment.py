import math
import yahoo_fin.stock_info as si
import pandas as pd
import datetime

#add check for if stock move to much and not on a fall trand over long time
def stock_info(stocks_symbols):
    time_period = 20
    date = str((datetime.datetime.now() - datetime.timedelta(days=time_period * 365)).date())
    print(date)
    for symbol in stocks_symbols:
        yearly_data = []
        stock = si.get_data(symbol, start_date=date, index_as_date=False)
        stock_dividends = si.get_dividends(symbol, start_date=date, index_as_date=False)
        print(stock.keys())
        print(stock_dividends.keys())
        for year in stock.groupby(stock.date.dt.year):
            dividend_sum = stock_dividends[stock_dividends.date.dt.year == year[0]]['dividend'].sum()
            start_price = year[1].head(1).adjclose.mean()
            end_price = year[1].tail(1).adjclose.mean()+dividend_sum
            yearly_data.append({
                'year': year[0],
                'close': str((end_price/start_price - 1)*100) + '%',
            })
        print(yearly_data)
        avg_volume = stock['volume'].mean()
        avg_price = stock['adjclose'].mean()
        today_volume = stock.tail(1).volume.mean()
        today_price = stock.tail(1).adjclose.mean()
        # print("Average volume for",symbol,"is",avg_volume)
        # print("Average price for", symbol, "is", avg_price)
        # print("Average price volume for",symbol,"is",avg_volume*avg_price)

        if avg_volume * avg_price > 20000000 and today_volume * today_price > 20000000:
            print("The stock", symbol, "is good")


def sigmaEq1(i, n, a):
    return a*((a**n)-1)/(a-1)


def main():
    current_salary = float(input("Enter your current salary: "))
    percent_raise = float(input("Enter the percent raise in %: "))
    current_savings = float(input("Enter the current savings: "))
    retierment_salery = float(input("Enter the retierment salary you want in bruto (25% tax): "))
    years = math.log10(300*(3*current_salary + 4*retierment_salery)/(percent_raise*current_savings + 900*current_salary)) / math.log10(1+percent_raise/100)
    to_save = current_savings*(1+percent_raise/100)**years + current_salary*12*(1+percent_raise/100)*((1+percent_raise/100)**years - 1)/(percent_raise/100)
    print("number of years",years)
    print("to save",to_save)


if __name__ == "__main__":
    main()
    #stock_info(["VOO"])