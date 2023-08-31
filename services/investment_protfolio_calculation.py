import yfinance as yf
import pandas as pd
from sklearn import linear_model
import sklearn
import matplotlib.pyplot as pyplot


def get_stock_yearly_returns(tic='voo', period='max', dividend_tax=0.25) -> pd.DataFrame:
    symbol = yf.Ticker(tic)
    history = symbol.history(period=period)
    dividends = symbol.dividends.groupby(symbol.dividends.index.year).sum()
    dividends = dividends.reindex(history.index.year.unique(), fill_value=0)
    yearly_history = history.groupby(history.index.year)
    return pd.DataFrame(
        (
                (
                    (yearly_history.apply(lambda x1: x1.loc[x1.index.max()]['Close']) + dividends * (1 - dividend_tax))
                    / yearly_history.apply(lambda x1: x1.loc[x1.index.min()]['Close'])
                ) - 1
        ) * 100, columns=["return"], index=history.index.year.unique()
    ).dropna()


if __name__ == '__main__':
    voo = get_stock_yearly_returns()
    sp500 = get_stock_yearly_returns(tic='^gspc')
    x = sp500.loc[sp500.index.isin(voo.index)]
    y_pred = sp500.loc[~sp500.index.isin(voo.index)]
    linear = linear_model.LinearRegression()
    linear.fit(x, voo)
    voo = voo.append(pd.DataFrame(linear.predict(y_pred), columns=["return"], index=y_pred.index)).sort_index()
    
    # print(f'all time avg return: {voo.mean()}')
    # for period in range(1, 60):
    #     print(f'{period} year avg return: {voo[-period:].mean()}')

