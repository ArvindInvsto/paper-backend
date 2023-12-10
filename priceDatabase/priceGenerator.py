import pandas as pd
import random
import pytz
from datetime import datetime


def get_spot_price(instrument: str) -> dict:
    retDic = {'Instrument': instrument, 'LTP': '', 'Volumne': ''}
    price = round(random.uniform(1000.00, 9999.00), 2)
    volumne = round(random.uniform(100000.00, 999999.00), 2)

    retDic['LTP'] = price
    retDic['Volumne'] = volumne

    return retDic


def hisPriceGenerator(instrument, startPrice, volatility, timeframe='1Min'):
    utcTimezone=pytz.timezone('UTC')
    start = datetime.now(utcTimezone).strftime('%d/%m/%Y')+' 00:00'
    end = datetime.now(utcTimezone)

    dt = pd.date_range(start=start, end=end,
                       freq=timeframe).strftime('%d/%m/%Y %H:%M')
    df = pd.DataFrame(columns=['Instrument', 'Open',
                      'High', 'Low', 'Close'])
    df['Datetime'] = dt
    df['Instrument'] = instrument
    df['timeframe'] = timeframe
    df.index = df['Datetime']
    df.drop(['Datetime'], axis=1, inplace=True)

    for d in df.index:
        low = startPrice-(startPrice*volatility)
        high = startPrice+(startPrice*volatility)
        startPrice = round(random.uniform(low, high), 2)
        high = round(random.uniform(
            startPrice, (startPrice+(startPrice*0.08))), 2)
        low = round(random.uniform(
            startPrice, (startPrice-(startPrice*0.08))), 2)
        open = round(random.uniform(low, high), 2)

        df.loc[d, 'Close'] = startPrice
        df.loc[d, 'Open'] = open
        df.loc[d, 'High'] = high
        df.loc[d, 'Low'] = low

    return df


def candleGenerator(instrument, startPrice, volatility, num):
    retList = []

    candleDic = {'Instrument': instrument, 'Open': '',
                 'High': '', 'Low': '', 'Close': ''}
    for i in range(num):
        low = startPrice-(startPrice*volatility)
        high = startPrice+(startPrice*volatility)
        startPrice = round(random.uniform(low, high), 2)
        high = round(random.uniform(startPrice, high), 2)
        low = round(random.uniform(startPrice, low), 2)
        open = round(random.uniform(low, high), 2)

        candleDic['Close'] = startPrice
        candleDic['Open'] = open
        candleDic['High'] = high
        candleDic['Low'] = low

        retList.append(candleDic)

    return retList
