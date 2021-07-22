import datetime as dt
import os
import pickle
import nsedata
import pandas
import wget
from icecream import ic

ic.enable()

NSE_urlList = {
    'ind_nifty500list.csv': 'https://www1.nseindia.com/content/indices/ind_nifty500list.csv',
    'ind_nifty200list.csv': 'https://www1.nseindia.com/content/indices/ind_nifty200list.csv',
    'ind_nifty100list.csv': 'https://www1.nseindia.com/content/indices/ind_nifty100list.csv',
    'ind_nifty50list.csv': 'https://www1.nseindia.com/content/indices/ind_nifty50list.csv'
    }


def save_nse_tickers(n: int = 50):
    """Downloads a csv file containing all the NSE[500/200/100/50] stocks.
    Extracts the symbols as tickers.
    Args:
        n (int, optional): Defines the number of tickers to be retrieved.
            Possible values are 50, 100, 200, 500. Default value is 50.
    Raises:
        ValueError: 'n' must be in the list[50, 100, 200, 500]")
    Returns:
        list: list of 'n' number of tickers
    """
    ic.enable()

    def check(n):
        if not(n in [50, 100, 200, 500]):
            raise ValueError("Sorry. 'n' must be in the list[50, 100, 200, 500]")

    fileName = f'ind_nifty{n}list.csv'
    os.chdir('./NSE_Lists/')

    # TODO: code to update file timely
    if not os.path.exists(fileName):
        wget.download(NSE_urlList[fileName])

    with open(fileName, 'r') as f:
        df = pandas.read_csv(f, chunksize=5)
        df2 = pandas.concat([chunk for chunk in df])
        # Company Name,Industry,Symbol,Series,ISIN Code

    tickerList = df2.query('Series == "EQ"')['Symbol'].tolist()
    ic(tickerList)
    with open(f'nse{n}tickers.pickle', 'wb') as f:
        pickle.dump(tickerList, f)

    os.chdir('../')
    return tickerList


def get_data_from_nsedata(reload_tickerList=False):
    ic.enable()
    nse = nsedata.Nse()
    tickers = ['reliance']
    # for i in range(5, 1):
    #     if n:int not in [50, 100, 200, 500]:
    #         n = int(input("Select NSE index components: 50, 100, 200, 500\n"))
    #         i -= 1

    # if reload_tickerList:
    #     tickers = save_nse_tickers(n)
    # else:
    #     with open('nse500tickers.pickle', 'rb') as f:
    #         tickers: list = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    start = dt.date(2000, 1, 1).strftime('(%Y, %m, %d)')
    end = dt.datetime.strptime(dt.datetime.now(), '(%Y, %m, %d)')

    for ticker in tickers:
        if not os.path.exists(f'stock_dfs/{ticker}.csv'):
            # nse.historical_data("reliance", (2020, 1, 1), (2021, 1, 1))
            data = nse.historical_data(ticker, start, end)
            df = pandas.DataFrame(data)
            df.to_csv(f'stock_dfs/{ticker}.csv')
        else:
            print(f'Already have {ticker}')


def main():
    get_data_from_nsedata(reload_tickerList=False)


if __name__ == '__main__':
    main()
