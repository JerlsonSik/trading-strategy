import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd


import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import requests
import xlsxwriter
import math
import csv
import ta
from datetime import datetime
# Define the strategy
class SimpleStrategy(Strategy):
    def init(self):
        # Calculate the moving averages
        self.ma10 = self.I(talib.SMA, self.data.Close, timeperiod=10)
        self.ma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)

    def next(self):
        # Generate buy signal
        if crossover(self.ma10, self.ma50):
            self.buy()

        # Generate sell signal
        elif crossover(self.ma50, self.ma10):
            self.sell()

# Load the ETHUSDT data
data = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_1Hour.csv')
print(data)
# data['Date'] = pd.to_datetime(data[0])
# data.set_index('Date', inplace=True)
# data.sort_index(inplace=True)

# Run the backtest with the strategy
bt = Backtest(data, SimpleStrategy)
result = bt.run()

# Print the backtest result
print(result)


# from backtesting import Backtest, Strategy
# from backtesting.lib import crossover

# from backtesting.test import SMA, GOOG


# class SmaCross(Strategy):
#     n1 = 10
#     n2 = 20

#     def init(self):
#         close = self.data.Close
#         self.sma1 = self.I(SMA, close, self.n1)
#         self.sma2 = self.I(SMA, close, self.n2)

#     def next(self):
#         if crossover(self.sma1, self.sma2):
#             self.buy()
#         elif crossover(self.sma2, self.sma1):
#             self.sell()


# bt = Backtest(GOOG, SmaCross,
#               cash=10000, commission=.002,
#               exclusive_orders=True)
# print(GOOG)
# output = bt.run()
# bt.plot()
# print(output)


#This is to use the Backtest Strategy 

# import numpy as np
# import pandas as pd
# from backtesting import Backtest, Strategy
# from backtesting.lib import crossover
# from backtesting.test import SMA
# import requests
# import xlsxwriter
# import math
# import csv
# import ta
# from datetime import datetime

# filename = 'ETHUSDT_1.1.2018-20.4.2023_5Minutes.csv'
# df=pd.read_csv(filename,usecols=[0,1,2,3,4,5],names=["Date","Open","High","Low","Close","Volume"])
# print(df)
# class SmaCross(Strategy):
#     def init(self):
#         #close = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[4],names=['Closing'])
#         price = self.data.Close
#         self.ma1 = self.I(SMA, price, 10)
#         self.ma2 = self.I(SMA, price, 20)

#     def next(self):
#         if crossover(self.ma1, self.ma2):
#             self.buy()
#         elif crossover(self.ma2, self.ma1):
#             self.sell()


# bt = Backtest(df, SmaCross, commission=.002,
#               exclusive_orders=True)
# stats = bt.run()
# bt.plot()
# print(stats)

#df = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv')
#df.head()
# time = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[0],names=['Time'])
# open = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[1],names=['Opening'])
# high = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[2],names=['High'])
# low = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[3],names=['Low'])
# close = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[4],names=['Closing'])
# volume = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv',usecols=[5],names=['Volumes'])

# HAClose = (open['Opening']+high['High']+low['Low']+close['Closing'])/4
# #heiClosing = pd.DataFrame()
# #heiClosing['heiClosing'] = round(((open['Opening']+high['High']+low['Low']+close['Closing'])/4),2)

# HAHigh = (high['High'])
# HALow = (low['Low'])
# data = pd.DataFrame()

# #data = pd.DataFrame()
# #data['Opening'] = HAOpen
# data['Closing'] = HAClose
# data['High'] = HAHigh
# data['Low'] = HALow
# print(data)


# SMA30 = pd.DataFrame()
# SMA30['SMA30'] = ethDay['Closing'].rolling(window=30).mean()
# SMA100 = pd.DataFrame()
# SMA100['SMA100'] = ethDay['Closing'].rolling(window=100).mean()
# heiClosing= pd.DataFrame()
# heiClosing['heiClosing'] = round(((ethDayOpen['Opening']+ethDayHigh['High']+ethDayLow['Low']+ethDay['Closing'])/4),2)
# heiOpening = pd.DataFrame()
# heiOpening['heiOpening'][0] = ethDayOpen['Opening'][0]
# print(ethDayOpen)

