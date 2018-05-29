from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import datetime

# Import the backtrader platform
import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds

# import extensions
from extensions.observer.ob_acctvalue import AcctValue
from extensions.datafeed.convert_raw_data import convert_raw_data_from_KI

# import strategies
from Strategies.strat_madiff import STRAT_MADIFF


'''
    1. cerebro를 만들고 데이터를 넣어준다.
    2. Broker -> Observer -> Strategy -> Analyzer -> Writer 순으로 정의
'''
if __name__ == '__main__' :

    cerebro = bt.Cerebro(stdstats=False)
    datapath = './resources/etc.csv'
    dataframe = convert_raw_data_from_KI(datapath)

    data = bt.feeds.PandasData(dataname=dataframe,
                               datetime=0
                               )
    # cerebro.adddata(data)
    cerebro.resampledata(dataname=data,
                         timeframe = bt.TimeFrame.Days)

    ''' -------------------------------------------------------------------  '''
    # Broker setting
    start_value = 10000000
    cerebro.broker.setcash(start_value)
    cerebro.broker.setcommission(commission=0.005)
    cerebro.addsizer(bt.sizers.PercentSizer)

    ''' -------------------------------------------------------------------  '''
    # Observer Setting
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(AcctValue)

    ''' -------------------------------------------------------------------  '''
    # Strategy Setting
    cerebro.addstrategy(STRAT_MADIFF)


    ''' -------------------------------------------------------------------  '''
    # Analyzer Setting
    # cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    # cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")


    ''' -------------------------------------------------------------------  '''
    # Writer Setting
    # cerebro.addwriter(bt.WriterFile, csv=True)


    ''' -------------------------------------------------------------------  '''
    # Run cerebro
    cerebro.run()


    # print the analyzers
    # printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    # printSQN(firstStrat.analyzers.sqn.get_analysis())

    ''' -------------------------------------------------------------------  '''
    # Plot the result
    cerebro.plot(style='candle')
