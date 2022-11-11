from backtesting import Backtest, Strategy
from backtesting.lib import crossover
 
import talib
import backtestingService

class EmaCrossShort(Strategy):
    n1 = 20
    n2 = 250

    def init(self):
        close = self.data.Close
        self.ema1 = self.I(talib.EMA, close, self.n1)
        self.ema2 = self.I(talib.EMA, close, self.n2)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.position.close()
        elif crossover(self.ema2, self.ema1):
            self.sell()

if __name__ == "__main__":
    backtestingService.runBacktest(
        backtestClass=EmaCrossShort, 
        optimisationParams={
            'n1':range(10, 60, 5),
            'n2':range(70, 300, 10),
            'constraint':lambda p: p.n1 < p.n2
            })

     

        