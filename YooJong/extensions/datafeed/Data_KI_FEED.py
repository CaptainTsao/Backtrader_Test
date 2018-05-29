import datetime
import backtrader.feeds as btfeed

class MyDataFeed(btfeed.GenericCSVData):
    params = (
        ('fromdate', datetime.datetime(2017, 10, 1)),
        ('todate',   datetime.datetime(2018,  5, 20)),
        ('nullvalue', 0.0),

        ('dtformat', ('%Y-%m-%d')),
        ('tmformat', ('%H:%M:%S')),

        ('datetime', 0),
        ('time', 1),
        ('volume', 2),
        ('high', 3),
        ('low', 4),
        ('open', 5),
        ('close', 6),
        ('openinterest', -1)
    )
