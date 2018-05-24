import pandas as pd
import numpy as np
from datetime import datetime

def convert_raw_data(raw_data_path):
    data = pd.read_csv(raw_data_path)
    data['timestamp'] = data['timestamp'].map(lambda x : datetime.fromtimestamp(int( x / 1000)))
    data.drop(columns=['accPrice', 'candleDateTime', 'candleDateTimeKst'], inplace=True)
    data.rename(columns={'timestamp' : 'datetime'}, inplace=True)
    data.to_csv('BTC_to_Backtrader.csv', index=False, sep=',', encoding='utf-8' )

    return data

data = '/Users/YooJong/Projects/SystemTrading/YooJong/btc.csv'
print(convert_raw_data(data))
