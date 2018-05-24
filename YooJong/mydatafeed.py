import datetime
import backtrader.feeds as btfeed

class MyDataFeed(btfeed.GenericCSVData):
    params = (
        ('fromdate', datetime.datetime(2017, 10, 1)),
        ('todate',   datetime.datetime(2018,  5, 20)),
        ('nullvalue', 0.0),

        ('datetime', 0),
        ('volume', 1),
        ('high', 2),
        ('low', 3),
        ('open', 4),
        ('close', 5),
        ('openinterest', -1)
    )
