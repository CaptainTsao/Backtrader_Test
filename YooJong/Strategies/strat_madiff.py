from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import datetime
import backtrader as bt
from backtrader.order import Order



class STRAT_MADIFF(bt.Strategy):
    params = (
         ('printlog', True),
    )
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # 기본 이동평균선
        self.sma_20 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=20)
        self.sma_60 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=60)

        # 지표 setting


    def log(self, message, dt=None, doprint=False):
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), message))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return
        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: {:,.2f}, Cost: {:,.2f}, Comm {:,.2f}'.format(
                     order.executed.price, order.executed.value, order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log(
                    'SELL EXECUTED, Price: {:,.2f}, Cost: {:,.2f}, Comm {:,.2f}'.format(
                     order.executed.price, order.executed.value, order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {:,.2f}, NET {:,.2f}'.format(
                 trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return
        self.diff_20 = self.sma_20[0] - self.sma_20[-1]
        if not self.position:

            # return
        # else:
            # return

    def stop(self):
        self.log('Ending Value {:,.2f}'.format(self.broker.getvalue()), doprint=True)
