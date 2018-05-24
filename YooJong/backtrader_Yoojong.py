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
from mydatafeed import MyDataFeed

# import extensions
from extensions.analyzer_v1 import printTradeAnalysis, printSQN, AcctValue
from extensions.convert_raw_data import convert_raw_data_from_csv

# import strategies
from Strategies.strat_1 import Strat1
from Strategies.UsingPrettyOSC import SimplePOC


if __name__ == '__main__' :

    cerebro = bt.Cerebro(stdstats=True)

    # Observer Setting (bt.Cerebro(stdstats = Falses))
    # cerebro.addobserver(AcctValue)
    # cerebro.addobserver(bt.broker)

    # Strategy setting
    cerebro.addstrategy(SimplePOC)

    # Feed Data into Cerebros
    # 주식 CSV파일 읽을 때
    #
    # datapath = './resources/Stock_Dataset(170706)/068270.csv'
    # data = convert_raw_data_from_csv(datapath)
    # data = bt.feeds.PandasData(dataname=data,
    #                            fromdate=datetime.datetime(2015, 1, 1)
    #                            )

    datapath = '/Users/YooJong/Programming/PythonProject/Backtrader_Test/YooJong/extensions/BTC_to_Backtrader.csv'
    data = MyDataFeed(dataname=datapath,
                      timeframe=bt.TimeFrame.Minutes, compression=30)
    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    # 기본 거래 크기, 수수료 세팅
    cerebro.addsizer(bt.sizers.PercentSizer)
    cerebro.broker.setcommission(commission=0.005)


    # Set our desired cash start
    start_value = 10000000
    cerebro.broker.setcash(start_value)


    # Analyzer setting
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
    cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")

    # Print out the starting conditions
    print('Starting Portfolio Value: {:,.2f}'.format(cerebro.broker.getvalue()))
    strategies = cerebro.run()
    firstStrat = strategies[0]

    port_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: {:,.2f}'.format(port_value))
    print('P/L : {:,}'.format(port_value - start_value))


    # print the analyzers
    printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
    printSQN(firstStrat.analyzers.sqn.get_analysis())
    # Plot the result
    cerebro.plot()
