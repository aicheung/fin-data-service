from backtesting import Backtest, Strategy
from backtesting.lib import crossover
 
import talib
import backtestingService

class EmaCross(Strategy):
    n1 = 20
    n2 = 250

    def init(self):
        close = self.data.Close
        self.ema1 = self.I(talib.EMA, close, self.n1)
        self.ema2 = self.I(talib.EMA, close, self.n2)

    def next(self):
        if crossover(self.ema1, self.ema2):
            self.buy()
        elif crossover(self.ema2, self.ema1):
            self.position.close()

if __name__ == "__main__":
    backtestingService.runBacktest(
        backtestClass=EmaCross, 
        optimisationParams={
            'n1':range(10, 60, 5),
            'n2':range(70, 300, 10),
            'constraint':lambda p: p.n1 < p.n2
            })

     

        