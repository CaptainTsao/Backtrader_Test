from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import datetime

import backtrader as bt


class SimplePOC(bt.Strategy):
    params = (
         ('printlog', True),
    )
    def __init__(self):
        self.dataclose = self.datas[0].close
        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.prettyosc = bt.indicators.PrettyGoodOscillator(
                             period = 20, plotname = 'prettyosc')

        self.ema_20 = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=20)
        '''
        self.ema_5 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=5)
        '''

    def log(self, message, dt=None, doprint=False):
        if self.params.printlog or doprint:

            date = self.datas[0].datetime.date(0).isoformat()
            time = self.datas[0].datetime.time(0).isoformat()

            dt = dt or (date + ' '+ time)

            print('%s, %s' % (dt, message))

            # dt = dt or self.datas[0].datetime.date(0)
            # print('%s, %s' % dt.isoformat(), message))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

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

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS {:,.2f}, NET {:,.2f}'.format(
                 trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return

        # 현재 Position을 가지고 있는지 확인을 한다.
        if not self.position:
            if self.prettyosc > 3 :
                self.log('BUY CREATE, {:,.2f}'.format(self.dataclose[0]))
                self.order = self.buy()

        # Long, buy 포지션을 갖고 있으면.
        else:
            if self.prettyosc < -3 :
                self.log('SELL CREATE, {:,.2f}'.format(self.dataclose[0]))
                self.order = self.sell()

    def stop(self):
        self.log('Ending Value {:,.2f}'.format(self.broker.getvalue()), doprint=False)
