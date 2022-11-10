import yfinance as yf

import argparse
from backtesting import Backtest
def runBacktest(backtestClass, optimisationParams):
    parser = argparse.ArgumentParser(description="EMA backtest")
    parser.add_argument("ticker", help="Ticker")
    parser.add_argument("--optimise", choices=['y', 'n'], default='n', help="Optimise", required=False)
    args = parser.parse_args()

    stock = args.ticker
    data = yf.Ticker(stock).history(period="max")

    bt = Backtest(data, backtestClass,
                cash = 100000, commission=.001,
                exclusive_orders=True)

    output = bt.run()
    bt.plot(open_browser=False)

    print(output)

    if args.optimise == 'y':
        print("OPTIMISE START")
        stats, heatmap = bt.optimize(
            **optimisationParams,
            constraint=lambda p: p.n1 < p.n2,
            maximize='Equity Final [$]',
            random_state=0,
            return_heatmap=True)


        print("BEST")
        print(stats)
        print("HEATMAP")
        print(heatmap.sort_values().iloc[-3:])