from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import talib
import backtestingService

class RsiCrossShort(Strategy):
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

        if self.rsiLowCrossed:
            self.position.close()
        elif self.rsiHighCrossed:
            self.sell()

if __name__ == "__main__":
    backtestingService.runBacktest(
        backtestClass=RsiCrossShort, 
        optimisationParams={
            'rsiHigh':range(50, 100, 1),
            'rsiLow':range(0, 49, 1),
            'constraint':lambda p: p.rsiLow < p.rsiHigh
        })
