from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA

import yfinance as yf

class SmaCross(Strategy):
    n1 = 10
    n2 = 200

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()


stock = "qqq"
data = yf.Ticker(stock).history(period="max")

bt = Backtest(data, SmaCross,
            cash = 100000, commission=.001,
            exclusive_orders=True)

output = bt.run()
bt.plot(open_browser=False)
print(output)

        