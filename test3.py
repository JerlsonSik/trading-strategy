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

def RSI_MA(data, period, ma_period):
    rsi = RSI(data, period)
    rsi_ma = talib.SMA(rsi, timeperiod=ma_period)
    return rsi, rsi_ma

def N_MACD(data, period):
    sh = talib.EMA(data, timeperiod=12)
    lon = talib.EMA(data, timeperiod=21)

    ratio = np.minimum(sh, lon) / np.maximum(sh, lon)
    mac = np.where(sh > lon, (2-ratio)-1, ratio-1)
    macNorm = ((mac - talib.MIN(mac, timeperiod=period)) / (talib.MAX(mac, timeperiod=period) - talib.MIN(mac, timeperiod=period) + 0.00001) * 2) - 1
    macNorm2 = np.where(sh < 2, mac, macNorm)
    trigger = talib.WMA(macNorm2, 9)

    return macNorm2, trigger

def SMA(data, period):
    return talib.SMA(data, timeperiod=period)

MARGIN = 2
LB = 5
class SikStrat(Strategy):

    def init(self):
        self.price_delta = 0.004
        self.rsi_period = 21
        self.rsi_ma_period = 55
        self.n_macd_period = 50
        self.sma_period = 13

        price = self.data.Close

        self.rsi, self.rsi_ma = self.I(RSI_MA, price, self.rsi_period, self.rsi_ma_period)

        self.macNorm2, self.trigger = self.I(N_MACD, price, self.n_macd_period)

        self.sma = self.I(SMA, price, self.sma_period)

    def next(self):
        if len(self.data) < LB: return

        # by default if we don't assign a size, it would be all in
        if self.rsi_ma <= 45:
            if crossover(self.macNorm2, self.trigger) and crossover(self.rsi, self.rsi_ma):
                current = self.data.Close[-1]
                sl = self.data.Low[-LB:].min()
                diff = abs(current - sl)
                tp = current + diff * MARGIN
                try:
                    # if signal appears, if we all in, unless the previous signal was short, or we dont have any position
                    # then we buy
                    if self.position.is_short or not self.position: 
                        self.buy(sl=sl, tp=tp)
                except: pass
        elif self.rsi_ma >= 55:
            if crossover(self.trigger, self.macNorm2) and crossover(self.rsi_ma, self.rsi):
                current = self.data.Close[-1]
                sl = self.data.High[-LB:].max()
                diff = abs(sl - current) 
                tp = current - diff * MARGIN
                try: 
                    # if signal appears, if we all in, unless the previous signal was long, or we dont have any position
                    # then we short
                    if self.position.is_long or not self.position: 
                        self.sell(sl=sl, tp=tp)
                except: pass


# class SmaCross(Strategy):
#     # Define the two MA lags as class variables
#     # for later optimization
#     n1 = 50
#     n2 = 100
    
#     def init(self):
#         # Precompute the two moving averages
#         self.sma1 = self.I(talib.SMA, self.data.Close, self.n1)
#         self.sma2 = self.I(talib.SMA, self.data.Close, self.n2)
    
#     def next(self):
#         # If sma1 crosses above sma2, close any existing
#         # short trades, and buy the asset
#         if crossover(self.sma1, self.sma2):
#             self.position.close()
#             self.buy()

#         # Else, if sma1 crosses below sma2, close any existing
#         # long trades, and sell the asset
#         elif crossover(self.sma2, self.sma1):
#             self.position.close()
#             self.sell()

# data = pd.read_csv("ETHUSDT_1.1.2023-15.6.2023_5Minutes.csv", index_col=0, parse_dates=True)
# data = pd.read_csv("ETHUSDT_1.1.2018-20.4.2023_5Minutes.csv", index_col=0, parse_dates=True)
data = pd.read_csv("ETHUSDT_1.1.2018-20.4.2023_5Minutes - Copy.csv")

data = data.iloc[10_000:]
bt = Backtest(data, SikStrat, commission=0.0003,
              exclusive_orders=True)
# bt = Backtest(data, SmaCross,
#               exclusive_orders=True)
stats = bt.run()
print()
print(bt._results)
# print(bt._results["_trades"].to_csv("trades.csv"))
bt.plot()

# print("Margin", MARGIN)
# print("LookBack candlestick", LB)

# res = bt._results["_trades"]
# winning_res = res[(res["PnL"] > 0)]

# prob = defaultdict(int)
# for index, row in winning_res.iterrows():
#     entry = int(row["EntryBar"])
#     exit = int(row["ExitBar"])
    
#     entry_range = data.iloc[entry:exit+1, :]
#     lookback_bars = data.iloc[entry-LB:entry, :]

    
#     if row["EntryPrice"] < row["ExitPrice"]: # buy
#         entry_low_range_before_profit = entry_range["Low"]
#         min_low = entry_low_range_before_profit.min()

#         values = (min_low - lookback_bars["Low"]).values # pos diff, means range low is higher
#         valid_idx = np.where(values > 0)[0]
#         if valid_idx.size == 0: prob[LB] += 1; continue
#         bar = valid_idx[values[valid_idx].argmin()]
#         # print(LB - bar, "th bar looking back")
#         prob[LB - bar] += 1
        
#     elif row["EntryPrice"] > row["ExitPrice"]: # sell
#         entry_high_range_before_profit = entry_range["High"]
#         max_high = entry_high_range_before_profit.max()

#         values = (lookback_bars["High"] - max_high).values # pos diff, means range high is lower
#         valid_idx = np.where(values > 0)[0]
#         if valid_idx.size == 0: prob[LB] += 1; continue
#         bar = valid_idx[values[valid_idx].argmin()]
#         # print(LB - bar, "th bar looking back")
#         prob[LB - bar] += 1

# for k, v in prob.items():
#     prob[k] = (v/len(winning_res)) * 100

# print(prob)