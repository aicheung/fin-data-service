from backtesting import Backtest, Strategy
from backtesting.lib import crossover

import talib

import yfinance as yf

class MacdCross(Strategy):
    fast = 12
    slow = 26
    signal = 9

    def init(self):
        close = self.data.Close
        self.macd, self.macdsignal, self.macdhist = self.I(talib.MACD, close, self.fast, self.slow, self.signal)

    def next(self):
        if crossover(self.macd, self.macdsignal):
            self.buy()
        elif crossover(self.macdsignal, self.macd):
            self.position.close()


stock = "spy"
data = yf.Ticker(stock).history(period="max")

bt = Backtest(data, MacdCross,
            cash = 100000, commission=.001,
            exclusive_orders=True)

output = bt.run()
bt.plot(open_browser=False)
print(output)

        