import datetime as dt
import os

# TODO: use finplot insted of pyplot
# from matplotlib.finance import candlestick_ohlc
# from mplfinance import candlestick2_ohlc
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
from icecream import ic
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib import style

ic.enable()
style.use('fast')

# TODO: save the Nifty500 ticker symbols in a file.
# TODO: fetch tickers as in NSE, as in yahoofinance, as in google, as in zerodha; and company name
# TODO: implement a function to fetch the data from the above sources and store to database

start = dt.datetime(2000, 1, 1)
# TODO: rewrite the enddate to be the current date.
end = dt.datetime(2021, 7, 21)
# end = dt.datetime.strftime(dt.datetime.now(), '%Y, %m, %d')

# todo: re-write the code to fetch the EOD data from the NSE website.
# TODO: re-write the code to fetch EOD data for each of the Nifty500 tickers.
# TODO: re-write the code to store the data to a database instead of a file.
if not os.path.exists('NSEI.csv'):
    df = web.DataReader('^NSEI', 'yahoo', start, end)
    df.to_csv('NSEI.csv')
else:
    df = pd.read_csv('NSEI.csv', parse_dates=True, index_col=0)

# ic(df.head())

# Resample the EOD data to Weekly interval ie 5days
ohlcv = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
df_ohlc = df.resample('5D').agg(ohlcv)
# ic(df_ohlc.tail())

df_ohlc['100ma'] = df_ohlc['Adj Close'].rolling(window=100, min_periods=0).mean()
# df.dropna(inplace=True)

# candlestick2_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
# ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)


ap0 = [mpf.make_addplot(df_ohlc['100ma'], color='b', panel=0)]
mpf.plot(data=df_ohlc, volume=True, type='candle', colorup='g', addplot=ap0, panel_ratios=(4, 1))


# ax1.plot(df.index, df['Adj Close'])
# ax1.plot(df.index, df['100ma'])
# ax2.bar(df.index, df['Volume'])

# plt.show()
