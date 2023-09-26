from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG, EURUSD

import talib
import pandas as pd
import numpy as np
from collections import defaultdict

def RSI(data, period):
    rsi = talib.RSI(data, timeperiod=period)
    return rsi

def MA(data, period):
    ma = talib.SMA(data,timeperiod=period)
    ma_50 = talib.SMA(data,timeperiod = period)
    ema = talib.EMA(ma,timeperiod=period)
    return ma,ma_50,ema

def VOLUME_MA(data,period):
    volume_ma = talib.SMA(data,timeperiod = period)
    return volume_ma


MARGIN = 2
LB = 5

class SikStrat(Strategy):

    def init(self):
        self.price_delta = 0.004
        self.rsi_period = 14
        self.ma_period = 10
        self.volume_period = 20

        price = self.data.Close
        volume = self.data.Volume

        self.rsi= self.I(RSI, price, self.rsi_period)

        self.ma, self.ma_50,self.ema = self.I(MA,price,self.ma_period)

        self.volume_ma = self.I(VOLUME_MA,volume,self.volume_period)
    
    def next(self):
        if len(self.data) < LB: return

        # by default if we don't assign a size, it would be all in
        if crossover(self.ma,self.ema) and self.data.Close > self.ma_50:
            if (self.rsi > 55 and self.rsi < 70) and (self.data.Close > self.data.Open) and (self.data.Low > self.ma) and (self.data.Volume > self.volume_ma):
                current = self.data.Close[-1]
                sl = self.ma
                diff = abs(current - sl)
                tp = current + diff * MARGIN
                try:
                    # if signal appears, if we all in, unless the previous signal was short, or we dont have any position
                    # then we buy
                    if self.position.is_short or not self.position: 
                        self.buy(sl=sl, tp=tp)
                except: pass
                
        elif crossover(self.ema,self.ma) and self.data.Close < self.ma_50:
            if (self.rsi > 30 and self.rsi < 45) and (self.data.Close < self.data.Open) and (self.data.High < self.ma) and (self.data.Volume > self.volume_ma):
                current = self.data.Close[-1]
                sl = self.ma
                diff = abs(sl - current) 
                tp = current - diff * MARGIN
                try:
                    # if signal appears, if we all in, unless the previous signal was long, or we dont have any position
                    # then we short
                    if self.position.is_long or not self.position: 
                        self.sell(sl=sl, tp=tp) 
                except: pass

#data = pd.read_csv("ETHBUSD_1.1.2023-2.8.2023_5Minutes.csv")
data = pd.read_csv("ETHUSDT_1.1.2018-20.4.2023_5Minutes - Copy.csv")

data = data.iloc[-1000000:]
bt = Backtest(data, SikStrat, commission=0.0003,
              exclusive_orders=True)
stats = bt.run()
print()
print(bt._results)
bt.plot()
