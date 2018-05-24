from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import datetime

import backtrader as bt


class Strat1(bt.Strategy):
    params = (
        ('maperiod', 15),
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

        # Add a MovingAverageSimple indicator
        # self.ema_5 = bt.indicators.ExponentialMovingAverage(
            # self.datas[0], period=5)
        self.ema_10 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=10, plotname='ema_10')
        self.ema_20 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=20, plotname='ema_20')
        self.ema_80 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=80, plotname='ema_80')
        '''
        self.ema_5 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=5)
        self.ema_10 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=10)
        self.ema_20 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=20)
        self.ema_40 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=40)
        self.ema_80 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=80)
        self.ema_160 = bt.indicators.ExponentialMovingAverage(
            self.datas[0], period=160)
        # self.ema_320 = bt.indicators.ExponentialMovingAverage(
            # self.datas[0], period=20)
        '''
        # Add Momentum
        self.prettyosc = bt.indicators.PrettyGoodOscillator(
                         period = 40, plotname = 'prettyosc')

    def log(self, message, dt=None, doprint=False):
        ''' Logging function fot this strategy'''

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
        # Simply log the closing price of the series from the reference
        # self.log('Close, {:,.2f}'.format(self.dataclose[0]))
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # 현재 Position을 가지고 있는지 확인을 한다.
        if not self.position:
            if self.prettyosc > 4.0 :
                self.log('BUY CREATE, {:,.2f}'.format(self.dataclose[0]))
                self.order = self.buy()
            # if self.datavolume[0] > 10 * self.datavolume[-1]:
                # self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # self.order = self.buy()
            # if self.ema_10[0] > self.ema_20[0]:
                # self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # order가 buy객체를 계속 traking해서 2개의 order를 만들지 않도록 한다.
                # self.order = self.buy()

        # Long, buy 포지션을 갖고 있으면.
        else:
            if self.dataclose[0] < self.ema_20[0]:
                self.log('SELL CREATE, {:,.2f}'.format(self.dataclose[0]))
                self.order = self.sell()

    def stop(self):
        self.log('Ending Value {:,.2f}'.format(self.broker.getvalue()), doprint=True)
