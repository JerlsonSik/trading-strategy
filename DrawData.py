from binance.client import Client
import config, csv
import numpy as np
import pandas as pd
import requests
# import xlswriter
import math
from datetime import datetime

client = Client(config.apiKey,config.apiSecurity)
print("Logged in")

#candles = client.get_klines(symbol='ETHUSDT', interval = Client.KLINE_INTERVAL_1DAY)

csvfile = open('ETHBUSD_1.1.2023-2.8.2023_5Minutes.csv','w',newline='')
candlestick_writer = csv.writer(csvfile,delimiter = ',')


#print(len(candles))
candlestick = client.get_historical_klines("ETHBUSD", Client.KLINE_INTERVAL_5MINUTE,"1 Jan, 2023","2 Aug, 2023")

# for i in range (len(candlestick)):
    
#     epochTime = candlestick[i][0]/1000
#     date_conv = datetime.fromtimestamp(epochTime)
    
#     candlestick_writer.writerow(candlestick[0][i]
for candlestick in candlestick:
    # print(candlestick[0])
    candlestick[0] = datetime.fromtimestamp(candlestick[0]/1000)
    candlestick_writer.writerow(candlestick)

csvfile.close
