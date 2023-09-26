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

filename = 'ETHUSDT_1.1.2018-31.5.2023_1hour.csv'
df=pd.read_csv(filename,usecols=[0,1,2,3,4,5],names=["Date","Open","High","Low","Close","Volume"])
csvfile = open('ETHUSDT_1.1.2018-31.5.2023_1hour_modified_2.csv','w+',newline='')
date = df["Date"]
open = df["Open"]
high = df["High"]
low = df["Low"]
close = df["Close"]
volume = df["Volume"]
date_and_time = date.str.split()

#csvfile = open('ETHUSDT_1.1.2018-31.5.2023_1hour_modified_2.csv','w+',newline='')
#candlestick_writer = csv.writer(csv,delimiter = ',')

print(type(df))
list = []
for i in range(len(date_and_time)):
    year_before_split = date_and_time[i][0]
    year = year_before_split.replace("-",".")
    time = date_and_time[i][1]
    openFinal = open[i]
    highFinal = high[i]
    lowFinal = low[i]
    closeFinal = close[i]
    volumeFinal = volume[i]
    list.append([year,time,openFinal,highFinal,lowFinal,closeFinal,volumeFinal])
    


with csvfile:
    write = csv.writer(csvfile)
    write.writerows(list)

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

# df = pd.read_csv('ETHUSDT_1.1.2018-1.1.2023_5Minutes.csv')
# df.head()
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

