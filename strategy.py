
import talib
import numpy as np

class SikStrat:

    MARGIN = 2
    
    def __init__(self, data):
        self.data = data
        self.price = data.Close
        self.line_building()

    def RSI(self, period):
        rsi = talib.RSI(self.price, timeperiod=period)
        return rsi

    def RSI_MA(self, period, ma_period):
        rsi = self.RSI(period)
        rsi_ma = talib.SMA(rsi, timeperiod=ma_period)
        return rsi, rsi_ma

    def N_MACD(self, period):
        sh = talib.EMA(self.price, timeperiod=12)
        lon = talib.EMA(self.price, timeperiod=21)

        sh = sh[20:]
        lon = lon[20:]

        ratio = np.minimum(sh, lon) / np.maximum(sh, lon)
        mac = np.where(sh > lon, (2-ratio)-1, ratio-1)
        macNorm = ((mac - talib.MIN(mac, timeperiod=period)) / (talib.MAX(mac, timeperiod=period) - talib.MIN(mac, timeperiod=period) + 0.00001) * 2) - 1
        # print("sh", sh)
        # print("mac", mac)
        # print("macNorm", macNorm)
        macNorm2 = np.where(sh < 2, mac, macNorm)
        trigger = talib.WMA(macNorm2, 9)

        return macNorm2, trigger
    
    def SMA(data, period):
        return talib.SMA(data, timeperiod=period)
    
    def crossover(series1, series2):
        """"
        Return `True` if `series1` just crossed over (above)
        `series2`.

            >>> crossover(self.price.Close, self.sma)
            True
        """
        try:
            return series1[-2] < series2[-2] and series1[-1] > series2[-1]
        except IndexError:
            return False

    def check_enough_data(self, period):
        return len(self.price) >= period
    
    def line_building(self):
        self.rsi_period = 21
        self.rsi_ma_period = 55
        self.n_macd_period = 50
        self.sma_period = 13

        assert self.check_enough_data(self.rsi_period), "Not Enough Data"
        assert self.check_enough_data(self.rsi_ma_period), "Not Enough Data"
        assert self.check_enough_data(self.n_macd_period), "Not Enough Data"
        assert self.check_enough_data(self.sma_period), "Not Enough Data"

        self.rsi, self.rsi_ma = self.RSI_MA(self.rsi_period, self.rsi_ma_period)

        self.macNorm2, self.trigger = self.N_MACD(self.n_macd_period)

        self.sma = self.SMA(self.sma_period)

    def trigger(self):
        
        LB = 5 # look back

        LAST = -1

        if self.rsi_ma[LAST] <= 45:
            if self.data.Close[LAST] > self.sma[LAST]:
                if self.crossover(self.macNorm2, self.trigger) and self.crossover(self.rsi, self.rsi_ma):
                    current = self.data.Close[-1]
                    sl = self.data.Low[-LB:].min()
                    diff = abs(current - sl)
                    tp = current + diff * self.MARGIN

                    return {
                        "status": "BUY",
                        "sl": sl,
                        "tp": tp,
                    }
        
        elif self.rsi_ma[LAST] >= 55:
            if self.data.Close[LAST] < self.sma[LAST]:
                if self.crossover(self.trigger, self.macNorm2) and self.crossover(self.rsi_ma, self.rsi):
                    current = self.data.Close[-1]
                    sl = self.data.High[-LB:].max()
                    diff = abs(sl - current) 
                    tp = current - diff * self.MARGIN

                return {
                    "status": "SELL",
                    "sl": sl,
                    "tp": tp
                }
            
        return {"status": "NA"}