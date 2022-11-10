from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import talib

import yfinance as yf

class MacdCross(Strategy):
    fast = 12
    slow = 26
    signal = 9

    rsiPeriod = 14
    rsiHigh = 70
    rsiLow = 30

    def init(self):
        close = self.data.Close
        self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, close, self.fast, self.slow, self.signal)
        self.rsi = self.I(talib.RSI, close, self.rsiPeriod)

        self.rsiHighCrossed = False
        self.rsiLowCrossed = False

    def checkRsi(self):
        """Check if RSI is above or below threashold, update variables if so"""
        #High
        if crossover(self.rsi, self.rsiHigh):
            self.rsiHighCrossed = True
            self.rsiLowCrossed = False
        elif crossover(self.rsiHigh, self.rsi):
            #cancel
            self.rsiHighCrossed = False
            self.rsiLowCrossed = False

        #Low
        if crossover(self.rsiLow, self.rsi):
            self.rsiLowCrossed = True
            self.rsiHighCrossed = False
        elif crossover(self.rsi, self.rsiLow):
            #cancel
            self.rsiLowCrossed = False
            self.rsiHighCrossed = False

    def next(self):
        self.checkRsi()

        if crossover(self.macd, self.macdsignal) & self.rsiLowCrossed:
            self.buy()
        elif crossover(self.macdsignal, self.macd) & self.rsiHighCrossed:
            self.position.close()



stock = "tlt"
data = yf.Ticker(stock).history(period="max")

bt = Backtest(data, MacdCross,
            cash = 100000, commission=.001,
            exclusive_orders=True)

output = bt.run()
bt.plot(open_browser=False)
print(output)

        