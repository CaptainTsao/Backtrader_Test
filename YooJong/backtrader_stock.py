import backtrader as bt
import backtrader.indicators as btind
import datetime
import pandas as pd
from pandas import Series, DataFrame
import random
from copy import deepcopy


class AcctValue(bt.Observer):
    alias = ('Value',)
    lines = ('value',)

    plotinfo = {"plot": True, "subplot": True}

    def next(self):
        self.lines.value[0] = self._owner.broker.getvalue()



if __name__ == '__main__' :
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.set_cash(1000000)
    cerebro.broker.setcommission(0.003)

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime(2016, 10, 31)
    is_first = True
    # Not the same set of symbols as in other blog posts
    symbols = ["AAPL", "GOOG", "MSFT", "AMZN", "YHOO", "SNY", "NTDOY", "IBM", "HPQ", "QCOM", "NVDA"]
    plot_symbols = ["AAPL", "GOOG", "NVDA"]
    #plot_symbols = []
    for s in symbols:
        data = bt.feeds.YahooFinanceData(dataname=s, fromdate=start, todate=end)
        if s in plot_symbols:
            if is_first:
                data_main_plot = data
                print(data)
                is_first = False
            else:
                data.plotinfo.plotmaster = data_main_plot
        else:
            data.plotinfo.plot = False
        cerebro.adddata(data)
    # cerebro.addobserver(AcctValue)#
    # cerebro.run()
