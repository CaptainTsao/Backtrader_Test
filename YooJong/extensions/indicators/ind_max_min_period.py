import backtrader as bt

class DummyInd(bt.Indicator):
    lines = ('maxline', 'minline',)

    params = (('period', 5),)

    def __init__(self):
        self.lines.maxline[0] = bt.Max()
        self.lines.minline[0] = bt.Min()
