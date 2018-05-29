import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime



def convert_raw_data_from_KI(raw_data_path):
    print("------    Converting Raw Data    ------")
    data = pd.read_csv(raw_data_path)
    data['timestamp'] = data['timestamp'].map(lambda x : datetime.fromtimestamp(int( x / 1000)))
    data['datetime'] = data['timestamp']
    # data['date'] = data['timestamp'].map(lambda x : list(str(x).split(' '))[0])
    # data['time'] = data['timestamp'].map(lambda x : list(str(x).split(' '))[1])
    data.drop(['timestamp'], axis=1, inplace=True)
    data.drop(['accPrice', 'candleDateTime', 'candleDateTimeKst'], axis=1, inplace=True)
    data = data[['datetime', 'volume', 'high', 'low', 'open', 'close']]
    # data = data[['date', 'time', 'volume', 'high', 'low', 'open', 'close']]
    # data.to_csv('BTC_to_Backtrader.csv', index=False, sep=',', encoding='utf-8' )
    return data

def convert_raw_data_from_csv(raw_data_path):
    data = pd.read_csv(raw_data_path)
    data.drop(['Code', 'Company', 'Up&Down', 'Rate'],axis=1, inplace=True)
    data['Date'] = data['Date'].map(lambda x : pd.to_datetime(x))
    data.set_index('Date', inplace=True)
    return data
